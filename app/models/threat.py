"""Threat model."""

from sqlalchemy import Column, Integer, String, DateTime, func, JSON, Enum
from datetime import datetime
import enum

from app.database import Base


class ThreatType(str, enum.Enum):
    """Types of threats."""
    MALWARE = "malware"
    INTRUSION = "intrusion"
    DDOS = "ddos"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    BRUTE_FORCE = "brute_force"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_EXFILTRATION = "data_exfiltration"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    PHISHING = "phishing"


class ThreatSeverity(str, enum.Enum):
    """Threat severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ThreatStatus(str, enum.Enum):
    """Threat status."""
    ACTIVE = "active"
    MITIGATED = "mitigated"
    FALSE_POSITIVE = "false_positive"
    ARCHIVED = "archived"


class Threat(Base):
    """Threat detection model."""
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    threat_type = Column(Enum(ThreatType), nullable=False)
    severity = Column(Enum(ThreatSeverity), nullable=False)
    source_ip = Column(String(45), nullable=True, index=True)  # IPv4/IPv6
    destination_ip = Column(String(45), nullable=True, index=True)
    description = Column(String(1000), nullable=False)
    status = Column(Enum(ThreatStatus), default=ThreatStatus.ACTIVE, nullable=False)
    detection_timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    signature_id = Column(String(255), nullable=True, index=True)
    rule_id = Column(String(255), nullable=True, index=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Threat(id={self.id}, type={self.threat_type}, severity={self.severity})>"
