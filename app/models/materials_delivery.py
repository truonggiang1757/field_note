from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

class ExtractStatus(str, Enum):
    """Status of the extraction task."""
    SUCCESS = "success"
    ERROR = "error"

class MaterialsDeliveryRequest(BaseModel):
    file_url: str = Field(...,)

class MaterialsDeliveryResponse(BaseModel):
    status: ExtractStatus = Field(...)
    data: Optional[Dict[str, Any]] = Field(None)
    processing_time: Optional[float] = Field(None)
    error_message: Optional[str] = Field(None)