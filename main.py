import os
import tempfile
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse

from src.components.input_handler import UserInputHandler
from src.components.S3_storage_service import S3Storage
from src.components.vector_db_client import VectorDBClient
from src.components.rag_engine import RAGEngine
from src.components.generative_ai import GenerativeAI
from src.logger import logging
from src.exception import CustomException


# Initialize services
input_handler = UserInputHandler()
s3_storage_service = S3Storage()
vector_db_client = VectorDBClient()
rag_engine = RAGEngine()
generative_ai = GenerativeAI()

app = FastAPI()


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint to verify API is running"""
    return JSONResponse(status_code=200, content={"message": "FinEduGuide API is running"})


@app.post("/upload-file")
async def upload_document(
    file: UploadFile = File(...),
    pdf_processing_method: Optional[str] = Form(None)
) -> JSONResponse:
    """
    Upload a document (PDF or TXT)

    Args:
        file: Uploaded file (PDF or TXT)
        pdf_processing_method: PDF processing method
            - "standard text extraction"
            - "ocr based extraction"
    """
    logging.info(f"Received file upload request: {file.filename}")
    # Validate file type
    if file.content_type not in ("application/pdf", "text/plain"):
        logging.error(f"Unsupported file type: {file.content_type}")
        return JSONResponse(status_code=400, content={"error": "Unsupported file type. Upload PDF or TXT only."})
    
    # Validate PDF processing method
    PDF_Processing_Method = None
    if file.content_type == "application/pdf":
        if not pdf_processing_method:
            return JSONResponse(status_code=400, content={"error": "pdf_processing_method is required for PDF files"})
        # Normalize method string
        PDF_Processing_Method = pdf_processing_method.strip().lower()
        # Validate method
        if PDF_Processing_Method not in ("standard text extraction", "ocr based extraction"):
            logging.error(f"Invalid PDF processing method: {PDF_Processing_Method}")
            return JSONResponse(status_code=400, content={"error": "Invalid PDF processing method. Use 'standard text extraction' or 'ocr based extraction'."})
    
    # Save file to temporary directory
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, file.filename)
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file.file.seek(0)
            logging.debug(f"File saved temporarily at: {temp_file_path}")
            
            # Process file
            try:
                logging.debug(f"Processing file: {file.filename}")
                documents = input_handler.process_file(temp_file_path, PDF_Processing_Method=PDF_Processing_Method)
                logging.debug(f"File processed successfully: {file.filename}")
            except CustomException as e:
                logging.error(f"File processing failed: {str(e)}")
                return JSONResponse(status_code=500,content={"error": "Failed to process file"})

            # Upload file to S3
            try:
                logging.debug(f"Uploading {file.filename} to S3")
                s3_storage_service.upload_file(temp_file_path, file.filename)   
                logging.debug(f"File uploaded to S3: {file.filename}")
            except CustomException as e:
                logging.error(f"S3 upload failed: {str(e)}")
                return JSONResponse(status_code=500, content={"error": "Failed to upload file to storage"})

            # Store embeddings in Vector DB
            try:
                logging.debug(f"Storing embeddings for {file.filename}")
                stored = vector_db_client.store_embeddings(documents)
                if stored:
                    logging.debug(f"Embeddings stored successfully for {file.filename}")
            except CustomException as e:
                logging.error(f"Vector DB storage failed: {str(e)}")
                return JSONResponse(status_code=500, content={"error": "Failed to store document embeddings"})
    except Exception as e:
        logging.error("Unexpected error during upload flow")
        return JSONResponse(status_code=500, content={"error": "Unexpected error occurred during file upload"})
    logging.info(f"File upload and processing completed: {file.filename}")
    return JSONResponse(status_code=200, content={"message": "File uploaded and processed successfully"})


@app.post("/generate-content")
async def generate_content(
    user_query: str = Form(...),
    task_type: str = Form(...)
) -> JSONResponse:
    """
    Generate content based on user question and task type.

    Args:
        user_question: The user's question or topic.
        task_type: The type of task to perform:
            - "Explain"
            - "Quiz"
            - "Summary"
    """
    logging.info(f"Received content generation request. Task: {task_type}")
    # Validate task type
    valid_tasks = ("explain", "quiz", "summary")
    task_type = task_type.strip().lower()
    if task_type not in valid_tasks:
        logging.error(f"Invalid task type: {task_type}")
        return JSONResponse(status_code=400, content={"error": f"Invalid task type. Valid options are: {', '.join(valid_tasks)}"})

    try:
        user_query = input_handler.parse_user_query(user_query)
    except CustomException as e:
        logging.error(f"User query parsing failed: {str(e)}")
        return JSONResponse(status_code=400, content={"error": "Query too short. Please provide a more detailed query."})
    
    try:
        # Retrieve context using RAG Engine
        context = rag_engine.retrieve_context(user_query, top_k=5, relevance_threshold=0.5)
        # Assemble prompt
        prompt = rag_engine.assemble_prompt(context, user_query, content_type=task_type)
        # Generate content using Generative AI
        if task_type == "explain":
            generated_content = generative_ai.generate_content(prompt)
            logging.info("Content generated successfully")
        elif task_type == "quiz":
            generated_content = generative_ai.generate_quiz(prompt)
            logging.info("Quiz generated successfully")
        elif task_type == "summary":
            generated_content = generative_ai.generate_summary(prompt)
            logging.info("Summary generated successfully")
        return JSONResponse(status_code=200, content=generated_content)
    except CustomException as e:
        logging.error(f"Content generation failed: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Failed to generate content"})
        