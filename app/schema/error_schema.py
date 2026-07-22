from pydantic import BaseModel
from typing import Optional,Any

class ErrorDetails(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    error: ErrorDetails
    request_id: Optional[str] = None
    timestamp: str