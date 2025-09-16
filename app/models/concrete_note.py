from pydantic import BaseModel, Field
from typing import Dict, Optional, Any
from enum import Enum

class ConcreteExtractStatus(str, Enum):
    """Status of the extraction task."""
    SUCCESS = "success"
    ERROR = "error"

class ConcreteExtractRequest(BaseModel):
    """LLM parameters for the extraction task."""
    file_url: str = Field(...)
    model_name: Optional[str] = Field("Qwen/Qwen3-8B")

class ConcreteExtractResponse(BaseModel):
    status: ConcreteExtractStatus = Field(..., description="The final status of the extraction task.")
    data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    error_message: Optional[str] = None