"""Network traffic model."""

from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger
from datetime import datetime

from app.database import Base


class NetworkTraffic(Base):
    """Network traffic monitoring model."""
    __tablename__ = "network_traffic"

    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String(45), nullable=False, index=True)
    destination_ip = Column(String(45), nullable=False, index=True)
    source_port = Column(Integer, nullable=True)
    destination_port = Column(Integer, nullable=True, index=True)
    protocol = Column(String(10), nullable=False)  # TCP, UDP, ICMP
    packet_count = Column(Integer, default=0)
    bytes_sent = Column(BigInteger, default=0)
    bytes_received = Column(BigInteger, default=0)
    status = Column(String(50), default="normal")  # normal, suspicious, blocked
    timestamp = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<NetworkTraffic(id={self.id}, src={self.source_ip}, dst={self.destination_ip})>"
