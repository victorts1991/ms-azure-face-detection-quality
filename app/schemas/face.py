from pydantic import BaseModel
from typing import Optional, Dict

class FaceAnalysisResponse(BaseModel):
    status: str
    face_id: Optional[str] = None
    storage_url: str
    message: str

class FaceValidationError(BaseModel):
    error: str
    details: Optional[Dict] = None
    service: str = "Azure Face API" 

class StorageError(BaseModel):
    error: str
    message: str
    service: str = "Azure Blob Storage"