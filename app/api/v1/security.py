"""General security endpoints and dashboards."""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.threat import Threat, ThreatStatus, ThreatSeverity, ThreatType
from app.models.log import Log
from app.models.network import NetworkTraffic

router = APIRouter()


@router.get("/security/dashboard")
def get_security_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get security dashboard metrics."""
    # Contar ameaças por status
    active_threats = db.query(Threat).filter(Threat.status == ThreatStatus.ACTIVE).count()
    critical_threats = (
        db.query(Threat)
        .filter(
            (Threat.status == ThreatStatus.ACTIVE)
            & (Threat.severity == ThreatSeverity.CRITICAL)
        )
        .count()
    )
    total_threats = db.query(Threat).count()

    # Últimas 24h
    last_24h = datetime.now() - timedelta(hours=24)
    threats_24h = db.query(Threat).filter(Threat.created_at >= last_24h).count()

    return {
        "system_health": 98.5,
        "threats_detected": active_threats,
        "critical_threats": critical_threats,
        "access_attempts": 2341,
        "blocked_attempts": 156,
        "data_protected_tb": 2.4,
        "threats_last_24h": threats_24h,
        "total_threats": total_threats,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/security/threats/by-type")
def get_threats_by_type(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, int]:
    """Get threat count by type."""
    results = db.query(Threat.threat_type, func.count(Threat.id)).group_by(
        Threat.threat_type
    ).all()
    return {str(threat_type): count for threat_type, count in results}


@router.get("/security/threats/by-severity")
def get_threats_by_severity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, int]:
    """Get threat count by severity."""
    results = db.query(Threat.severity, func.count(Threat.id)).group_by(
        Threat.severity
    ).all()
    return {str(severity): count for severity, count in results}


@router.get("/security/network-activity")
def get_network_activity(
    hours: int = Query(24, ge=1, le=720),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get network activity metrics."""
    since = datetime.now() - timedelta(hours=hours)
    traffic = db.query(NetworkTraffic).filter(NetworkTraffic.timestamp >= since).all()

    total_packets = sum(t.packet_count for t in traffic)
    total_bytes_sent = sum(t.bytes_sent for t in traffic)
    total_bytes_received = sum(t.bytes_received for t in traffic)

    return {
        "total_packets": total_packets,
        "total_bytes_sent": total_bytes_sent,
        "total_bytes_received": total_bytes_received,
        "connections": len(traffic),
        "period_hours": hours,
        "average_packet_size": (
            (total_bytes_sent + total_bytes_received) / total_packets
            if total_packets > 0
            else 0
        ),
    }
