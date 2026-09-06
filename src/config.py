import os
from dotenv import load_dotenv
from src.exceptions import ConfigurationError

load_dotenv()

class Config:
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.cohere.com/v1/chat") 
    LLM_MODEL = os.getenv("LLM_MODEL", "command-r-plus")
    
    # If on Vercel, we must write to the ephemeral /tmp/ directory
    _db_path = "data/scigenius.db"
    if os.getenv("VERCEL") == "1":
        _db_path = "/tmp/scigenius.db"
        
    DATABASE_PATH = os.getenv("DATABASE_PATH", _db_path)
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7")) 
    
    @classmethod
    def validate(cls):
        if not cls.LLM_API_KEY:
            raise ConfigurationError("LLM_API_KEY environment variable is not set. Please set it in your .env file.")

config = Config()
