import sys
import os
import re
from typing import List, Dict
import fitz
import easyocr
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.logger import logging
from src.exception import CustomException



class ProcessFileUtils:
    def __init__(self) -> None:
        pass


    ## Standard Text Extraction
    def extract_pdf_text(self, file_path: str) -> str:
        try:
            logging.info(f"Extracting text from PDF: {file_path}")
            doc = fitz.open(file_path)
            text = ""
            for page_num, page in enumerate(doc):
                text += page.get_text()
                logging.debug(f"Extracted text from page {page_num + 1}")
            doc.close()
            logging.info(f"Successfully extracted {len(text)} characters from PDF")
            return text
        except Exception as e:
            logging.error(f"Error extracting PDF text: {str(e)}")
            raise CustomException(e, sys)
        

    ## OCR-based Extraction
    def extract_pdf_text_with_ocr(self, file_path: str) -> str:
        logging.info(f"Extracting text from PDF using OCR: {file_path}")
        try:
            reader = easyocr.Reader(['en'], gpu=False)
            doc = fitz.open(file_path)
            text = ""
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap()
                img_path = f"temp_page_{page_num + 1}.png"
                pix.save(img_path)
                ocr_result = reader.readtext(img_path, detail=0)
                page_text = " ".join(ocr_result)
                text += page_text + "\n"
                os.remove(img_path)
                logging.debug(f"OCR extracted text from page {page_num + 1}")
            doc.close()
            logging.info(f"Successfully extracted {len(text)} characters from PDF using OCR")
            return text
        except Exception as e:
            logging.error(f"Error extracting PDF text with OCR: {str(e)}")
            raise CustomException(e, sys)
        

    ## Txt file text Extraction
    def extract_txt_text(self, file_path: str) -> str:
        logging.info(f"Extracting text from TXT file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            logging.info(f"Successfully extracted {len(text)} characters from TXT file")
            return text
        except Exception as e:
            logging.error(f"Error extracting TXT text: {str(e)}")
            raise CustomException(e, sys)
        

    ## Cleaning text
    def clean_text(self, text: str) -> str:
        try:
            logging.info("Starting text cleaning")
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'[^\w\s.,!?;:\-\'\"()]', '', text)
            text = re.sub(r' +', ' ', text)
            cleaned_text = text.strip()
            logging.info("Text cleaning completed")
            return cleaned_text
        except Exception as e:
            logging.error(f"Error cleaning text: {str(e)}")
            raise CustomException(e, sys)


    ## text chunking using RecursiveCharacterTextSplitter with metadata
    def generate_chunk_metadata(self, file_path: str, chunk_index: int,chunk_text: str, chunk_size: int, chunk_overlap: int) -> Dict:
        logging.info(f"Generating metadata for chunk {chunk_index} from file {file_path}")
        try:
            filename = os.path.basename(file_path)
            metadata = {
                "source": filename,
                "chunk_index": chunk_index,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "text": chunk_text
            }
            logging.info(f"Metadata for chunk {chunk_index} generated")
            return metadata
        except Exception as e:
            logging.error(f"Error generating metadata for chunk {chunk_index}: {str(e)}")
            raise CustomException(e, sys)
        

    ## text chunking using RecursiveCharacterTextSplitter with metadata
    def chunk_text(self, text: str, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
        logging.info("Starting text chunking")
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators = ["\n\n", "\n", ".", " ", ""]
            )
            chunks = text_splitter.split_text(text)
            documents = []
            for idx, chunk in enumerate(chunks):
                metadata = self.generate_chunk_metadata(file_path, idx, chunk, chunk_size, chunk_overlap)
                document = Document(page_content=chunk, metadata=metadata)
                documents.append(document)
            logging.info(f"Text chunking completed: {len(documents)} chunks created")
            return documents
        except Exception as e:
            logging.error(f"Error during text chunking: {str(e)}")
            raise CustomException(e, sys)