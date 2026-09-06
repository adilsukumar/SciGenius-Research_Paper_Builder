import os
from dotenv import load_dotenv
from src.exceptions import ConfigurationError

load_dotenv()

class Config:
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.cohere.com/v1/chat") 
    LLM_MODEL = os.getenv("LLM_MODEL", "command-r-plus")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/scigenius.db")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7")) 
    
    @classmethod
    def validate(cls):
        if not cls.LLM_API_KEY:
            raise ConfigurationError("LLM_API_KEY environment variable is not set. Please set it in your .env file.")

config = Config()
