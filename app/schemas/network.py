"""Network traffic schemas."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NetworkTrafficCreate(BaseModel):
    """Network traffic creation schema."""
    source_ip: str = Field(..., min_length=7, max_length=45)
    destination_ip: str = Field(..., min_length=7, max_length=45)
    source_port: Optional[int] = Field(None, ge=1, le=65535)
    destination_port: Optional[int] = Field(None, ge=1, le=65535)
    protocol: str = Field(..., min_length=3, max_length=10)  # TCP, UDP, ICMP
    packet_count: int = Field(0, ge=0)
    bytes_sent: int = Field(0, ge=0)
    bytes_received: int = Field(0, ge=0)
    status: str = Field("normal", min_length=3, max_length=50)


class NetworkTrafficResponse(BaseModel):
    """Network traffic response schema."""
    id: int
    source_ip: str
    destination_ip: str
    source_port: Optional[int]
    destination_port: Optional[int]
    protocol: str
    packet_count: int
    bytes_sent: int
    bytes_received: int
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True
