"""SSL/TLS Certificate model."""

from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime

from app.database import Base


class SSLCertificate(Base):
    """SSL/TLS Certificate model."""
    __tablename__ = "ssl_certificates"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, unique=True, index=True)
    issuer = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=True)
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False, index=True)
    certificate_pem = Column(String(5000), nullable=False)
    key_pem = Column(String(5000), nullable=True)  # Should be encrypted
    fingerprint_sha256 = Column(String(255), nullable=True, unique=True, index=True)
    status = Column(String(50), default="valid")  # valid, expired, expiring
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<SSLCertificate(id={self.id}, domain={self.domain}, status={self.status})>"
