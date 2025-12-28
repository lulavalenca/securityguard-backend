"""Audit log model."""

from sqlalchemy import Column, Integer, String, DateTime, func, JSON, ForeignKey
from datetime import datetime

from app.database import Base


class AuditLog(Base):
    """Audit trail model."""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(255), nullable=False, index=True)
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_resource = Column(String(255), nullable=False, index=True)
    changes = Column(JSON, nullable=True)  # Before/after values
    ip_address = Column(String(45), nullable=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.target_resource})>"
