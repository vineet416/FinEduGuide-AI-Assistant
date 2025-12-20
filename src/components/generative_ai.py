import sys
from euriai.langchain import create_chat_model

from src.config import Config
from src.logger import logging
from src.exception import CustomException


class GenerativeAI:
    def __init__(self):
        logging.info("Initializing GenerativeAI component")
        self.api_key = Config.EURIAI_API_KEY
        self.LLaMA_4_SCOUT_MODEL = Config.LLaMA_4_SCOUT_MODEL
        self.GPT_4_1_NANO_MODEL = Config.GPT_4_1_NANO_MODEL
        self.GEMINI_2_5_FLASH_MODEL = Config.GEMINI_2_5_FLASH_MODEL
        self.TEMPERATURE = Config.TEMPERATURE
        logging.info("GenerativeAI component initialized successfully")


    def generate_content(self, prompt: str) -> str:
        try:
            logging.info("Generating content using LLaMA 4 Scout model")
            explanation_model = create_chat_model(
                api_key=self.api_key,
                model=self.LLaMA_4_SCOUT_MODEL,
                temperature=self.TEMPERATURE
            )
            response = explanation_model.invoke(prompt)
            logging.info("Content generated successfully")
            return response.content
        except Exception as e:
            logging.error(f"Error generating content: {str(e)}")
            raise CustomException(e, sys)


    def generate_quiz(self, prompt: str) -> str:
        try:
            logging.info("Generating quiz using GPT-4.1 Nano model")
            quiz_model = create_chat_model(
                api_key=self.api_key,
                model=self.GPT_4_1_NANO_MODEL,
                temperature=self.TEMPERATURE
            )
            response = quiz_model.invoke(prompt)
            logging.info("Quiz generated successfully")
            return response.content
        except Exception as e:
            logging.error(f"Error generating quiz: {str(e)}")
            raise CustomException(e, sys)

    
    def generate_summary(self, prompt: str) -> str:
        try:
            logging.info("Generating summary using Gemini 2.5 Flash model")
            summary_model = create_chat_model(
                api_key=self.api_key,
                model=self.GEMINI_2_5_FLASH_MODEL,
                temperature=self.TEMPERATURE
            )
            response = summary_model.invoke(prompt)
            logging.info("Summary generated successfully")
            return response.content
        except Exception as e:
            logging.error(f"Error generating summary: {str(e)}")
            raise CustomException(e, sys)