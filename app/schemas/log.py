"""Log schemas."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict


class LogCreate(BaseModel):
    """Log creation schema."""
    event_type: str = Field(..., min_length=3, max_length=100)
    action: str = Field(..., min_length=1, max_length=255)
    resource: Optional[str] = Field(None, max_length=255)
    status: str = Field(..., min_length=3, max_length=50)  # success, failure, pending
    source_ip: Optional[str] = None
    user_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class LogResponse(BaseModel):
    """Log response schema."""
    id: int
    event_type: str
    action: str
    resource: Optional[str]
    status: str
    source_ip: Optional[str]
    user_id: Optional[int]
    details: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True
