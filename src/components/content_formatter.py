import sys
from euriai.langchain import create_chat_model

from src.config import Config
from src.logger import logging
from src.exception import CustomException



class ContentFormatter:
    def __init__(self):
        try:
            logging.info("Initializing ContentFormatter component")
            self.format_model = create_chat_model(
                api_key=Config.EURIAI_API_KEY,
                model=Config.LLaMA_4_SCOUT_MODEL,
                temperature=Config.TEMPERATURE
            )
            logging.info("ContentFormatter component initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing ContentFormatter model: {str(e)}")
            raise CustomException(e, sys)


    def format_content(self, content: str) -> str:
        try:
            logging.info("Formatting content using LLaMA 4 Scout model")
            format_model = self.format_model
            prompt = f"""Please format the following content appropriately to enhance readability and engagement.
            note: Do not start your answer like this 'Here is the reformatted content...':
            \n\n{content}"""
            response = format_model.invoke(prompt)
            logging.info("Content formatted successfully")
            return response.content
        except Exception as e:
            logging.error(f"Error occurred while formatting content: {str(e)}")
            raise CustomException(e, sys)


    def format_quiz(self, quiz: str) -> str:
        try:
            logging.info("Formatting quiz using LLaMA 4 Scout model")
            format_model = self.format_model
            prompt = f"""Please format the following quiz to make it more engaging and clear. 
            note: Do not start your answer like this 'Here is the reformatted quiz to make it more engaging and clear...':
            \n\n{quiz}"""
            response = format_model.invoke(prompt)
            logging.info("Quiz formatted successfully")
            return response.content
        except Exception as e:
            logging.error(f"Error occurred while formatting quiz: {str(e)}")
            raise CustomException(e, sys)