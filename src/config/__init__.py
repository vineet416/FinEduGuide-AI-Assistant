import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EURIAI_API_KEY = os.getenv('EURIAI_API_KEY')
    OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
    LLaMA_4_SCOUT_MODEL = "llama-4-scout-17b-16e-instruct"
    GPT_4_1_NANO_MODEL = "gpt-4.1-nano"
    GEMINI_2_5_FLASH_MODEL = "gemini-2.5-flash"
    TEMPERATURE = 0.3

    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX_NAME = 'fineduguide-index'

    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET_NAME = 'fineduguide-bucket'