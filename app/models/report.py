"""Report model."""

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, LargeBinary
from datetime import datetime

from app.database import Base


class Report(Base):
    """Report model."""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(100), nullable=False)  # executive, technical, compliance
    title = Column(String(255), nullable=False)
    content = Column(String(50000), nullable=False)  # HTML/PDF content
    pdf_content = Column(LargeBinary, nullable=True)  # Binary PDF data
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, type={self.report_type}, title={self.title})>"
