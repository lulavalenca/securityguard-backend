"""Threat schemas."""

from pydantic import BaseModel, Field, IPvAnyAddress
from datetime import datetime
from typing import Optional, Any, Dict
from app.models.threat import ThreatType, ThreatSeverity, ThreatStatus


class ThreatBase(BaseModel):
    """Threat base schema."""
    threat_type: ThreatType
    severity: ThreatSeverity
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    description: str = Field(..., min_length=10, max_length=1000)
    signature_id: Optional[str] = None
    rule_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ThreatCreate(ThreatBase):
    """Threat creation schema."""
    pass


class ThreatUpdate(BaseModel):
    """Threat update schema."""
    severity: Optional[ThreatSeverity] = None
    status: Optional[ThreatStatus] = None
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    details: Optional[Dict[str, Any]] = None


class ThreatResponse(ThreatBase):
    """Threat response schema."""
    id: int
    status: ThreatStatus
    detection_timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ThreatFilter(BaseModel):
    """Threat filter schema."""
    threat_type: Optional[ThreatType] = None
    severity: Optional[ThreatSeverity] = None
    status: Optional[ThreatStatus] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
