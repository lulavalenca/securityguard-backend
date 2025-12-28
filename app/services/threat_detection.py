"""Threat detection service."""

from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.models.threat import Threat, ThreatType, ThreatSeverity, ThreatStatus


class ThreatDetectionService:
    """Threat detection logic."""

    def __init__(self, db: Session):
        self.db = db

    def analyze_network_traffic(self, src_ip: str, dst_ip: str, data: Dict[str, Any]) -> bool:
        """Analyze network traffic for threats."""
        # Simulated threat detection logic
        suspicious_patterns = {
            "syn_flood": data.get("packet_count", 0) > 1000,
            "port_scan": data.get("destination_port") in [22, 23, 3306, 5432],
        }
        return any(suspicious_patterns.values())

    def create_threat_record(
        self,
        threat_type: ThreatType,
        severity: ThreatSeverity,
        source_ip: str,
        destination_ip: str,
        description: str,
        details: Dict[str, Any] = None,
    ) -> Threat:
        """Create a threat record."""
        threat = Threat(
            threat_type=threat_type,
            severity=severity,
            source_ip=source_ip,
            destination_ip=destination_ip,
            description=description,
            details=details or {},
            status=ThreatStatus.ACTIVE,
        )
        self.db.add(threat)
        self.db.commit()
        self.db.refresh(threat)
        return threat

    def mitigate_threat(self, threat_id: int, notes: str = None) -> Threat:
        """Mark threat as mitigated."""
        threat = self.db.query(Threat).filter(Threat.id == threat_id).first()
        if threat:
            threat.status = ThreatStatus.MITIGATED
            self.db.commit()
            self.db.refresh(threat)
        return threat
