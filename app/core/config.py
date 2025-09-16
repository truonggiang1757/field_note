from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

class Settings(BaseSettings):

    MODEL_LLM: Optional[str] = os.getenv("MODEL_LLM") or "gemini-2.5-flash"
    MODEL_EMBEDDINGS: Optional[str] = os.getenv("MODEL_EMBEDDINGS") or "text-embedding-004"

    QWEN_LLM_URL: Optional[str] = os.getenv("QWEN_LLM_URL") 
    QWEN_EMBEDDING_URL: Optional[str] = os.getenv("QWEN_EMBEDDING_URL")

    VINTERN_LLM_URL: Optional[str] = os.getenv("VINTERN_LLM_URL")
    VINTERN_MODEL: str = "5CD-AI/Vintern-3B-R-beta"

    # API Settings
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "HR Agents API"
    APP_VERSION: str = "1.0.0"
    
    # Project Settings
    PROJECT_NAME: str = "HR Agents"
    DESCRIPTION: str = "Unified API for HR-related services"
    VERSION: str = "1.0.0"
    
    # Model settings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    MODEL_TEMPERATURE: float = 0.7
    QWEN_TOKEN: Optional[str] = os.getenv("QWEN_TOKEN")

    MAX_FILE_SIZE_MB: int = 50
    DEFAULT_TARGET_COLUMNS: str = "no,code,name,unit,brand,country,quantity,price,amount,note,materialPrice,laborPrice,workDevicePrice,materialAmount,laborAmount,workDeviceAmount"

    @property
    def MAX_FILE_SIZE_BYTES(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    # Template settings
    TEMPLATES_DIR: str = "app/templates"

    API_KEY: Optional[str] = os.getenv("API_KEY")
    API_KEY_NAME: Optional[str] = os.getenv("API_KEY_NAME")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 