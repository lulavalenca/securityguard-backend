"""Security policy model."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from datetime import datetime

from app.database import Base


class SecurityPolicy(Base):
    """Security policy model."""
    __tablename__ = "security_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(String(2000), nullable=True)
    trigger_event = Column(String(255), nullable=False)  # Condition that triggers action
    action = Column(String(255), nullable=False)  # Action to execute
    enabled = Column(Boolean, default=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<SecurityPolicy(id={self.id}, name={self.name}, enabled={self.enabled})>"
