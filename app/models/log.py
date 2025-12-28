"""Audit log model."""

from sqlalchemy import Column, Integer, String, DateTime, func, JSON, ForeignKey
from datetime import datetime

from app.database import Base


class Log(Base):
    """Event log model."""
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source_ip = Column(String(45), nullable=True, index=True)
    action = Column(String(255), nullable=False)
    resource = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)  # success, failure, pending
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Log(id={self.id}, event_type={self.event_type}, status={self.status})>"
