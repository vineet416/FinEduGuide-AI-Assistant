import re
import sys
from typing import Dict

from src.utils.process_file_utils import ProcessFileUtils
from src.logger import logging
from src.exception import CustomException



class UserInputHandler:
    def __init__(self):
        self.utils = ProcessFileUtils()


    def parse_user_query(self, query: str) -> str:
        try:
            logging.info(f"Parsing user query: {query}")
            topic = query.strip()
            topic = re.sub(r'[<>\"\'/\\]', '', topic)
            topic = re.sub(r'\s+', ' ', topic)
            if not (5 <= len(topic)):
                raise ValueError("Query too short. Please provide a more detailed query.") 
            logging.info(f"Parsed user query: {topic}")
            return topic
        except Exception as e:
            logging.error(f"Error parsing user query: {str(e)}")
            raise CustomException(e, sys)
        

    def process_file(self, file_path, PDF_Processing_Method: str = None) -> Dict:
        """
        Process the uploaded file and return chunked documents.
        Args:
            file_path (str): Path to the uploaded file.
            PDF_Processing_Method (str, optional): Method for processing PDF files. Defaults to None.
        
        PDF_Processing_Method: "standard text extraction" or "ocr based extraction"
        """
        try:
            logging.info(f"Processing file: {file_path} with PDF_Processing_Method: {PDF_Processing_Method}")
            PDF_Processing_Method = PDF_Processing_Method.strip().lower() if PDF_Processing_Method else None
            text = ""
            if file_path.endswith('.pdf'):
                # Text extraction for PDF
                if PDF_Processing_Method == "standard text extraction":  ## Using PyMuPDF
                    text += self.utils.extract_pdf_text(file_path)
                elif PDF_Processing_Method == "ocr based extraction":                                                    
                    text += self.utils.extract_pdf_text_with_ocr(file_path) ## Using easyocr
                else:
                    raise ValueError("Invalid PDF Processing Method. Choose 'standard text extraction' or 'ocr based extraction'")
            # Reading txt file using utf-8 encoding
            elif file_path.endswith('.txt'):                             
                    text += self.utils.extract_txt_text(file_path)
            else:
                raise ValueError("Only PDF, TXT files supported")
            logging.debug(f"Extracted {len(text)} characters from file")
        except Exception as e:
            logging.error(f"Error extracting text from file: {str(e)}")
            raise CustomException(e, sys)
        
        try:
            logging.debug("Cleaning and chunking extracted text")
            # Clean the text
            cleaned_text = self.utils.clean_text(text)
            # Chunk the text with file_path with metadata
            documents = self.utils.chunk_text(cleaned_text, file_path, chunk_size=1000, chunk_overlap=200)
            logging.info("File processing completed successfully")
            return documents
        except Exception as e:
            logging.error(f"Error processing file: {str(e)}")
            raise CustomException(e, sys)