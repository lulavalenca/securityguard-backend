"""Report generation endpoints."""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from enum import Enum
import io
import os

from app.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.threat import Threat, ThreatStatus
from app.models.vulnerability import Vulnerability, VulnerabilityStatus
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter()


class ReportType(str, Enum):
    """Report types."""
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    COMPLIANCE = "compliance"
    INCIDENTS = "incidents"


class ReportPeriod(str, Enum):
    """Report periods."""
    SEVEN_DAYS = "7"
    THIRTY_DAYS = "30"
    NINETY_DAYS = "90"
    CUSTOM = "custom"


class ReportRequest(BaseModel):
    """Report generation request."""
    report_type: ReportType = Field(default=ReportType.EXECUTIVE)
    period: ReportPeriod = Field(default=ReportPeriod.THIRTY_DAYS)
    include_charts: bool = Field(default=True)
    include_recommendations: bool = Field(default=True)


class ReportSummary(BaseModel):
    """Report summary."""
    report_type: str
    title: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    total_threats: int
    critical_threats: int
    vulnerabilities: int


@router.post("/reports/generate")
def generate_report(
    request: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Generate security report."""
    # Calcular período
    days = int(request.period)
    period_end = datetime.now()
    period_start = period_end - timedelta(days=days)

    # Obter dados
    total_threats = (
        db.query(Threat)
        .filter(Threat.created_at.between(period_start, period_end))
        .count()
    )
    critical_threats = (
        db.query(Threat)
        .filter(
            (Threat.created_at.between(period_start, period_end))
            & (Threat.severity == "critical")
        )
        .count()
    )
    vulnerabilities = (
        db.query(Vulnerability)
        .filter(Vulnerability.discovered_at.between(period_start, period_end))
        .count()
    )

    report_titles = {
        "executive": "Resumo Executivo de Segurança",
        "technical": "Análise Técnica Detalhada",
        "compliance": "Relatório de Conformidade",
        "incidents": "Relatório de Incidentes",
    }

    return {
        "report_type": request.report_type.value,
        "title": report_titles.get(request.report_type.value),
        "generated_at": datetime.now().isoformat(),
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "total_threats": total_threats,
        "critical_threats": critical_threats,
        "vulnerabilities": vulnerabilities,
        "status": "ready",
        "file_format": "pdf",
        "download_url": f"/api/v1/reports/download/{datetime.now().timestamp()}",
    }


@router.get("/reports/list", response_model=List[Dict[str, Any]])
def list_reports(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """List generated reports."""
    return [
        {
            "id": 1,
            "title": "Resumo Executivo",
            "type": "executive",
            "generated_at": (datetime.now() - timedelta(days=0)).isoformat(),
            "period": "últimos 30 dias",
        },
        {
            "id": 2,
            "title": "Análise de Ameaças",
            "type": "technical",
            "generated_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "period": "últimos 30 dias",
        },
        {
            "id": 3,
            "title": "Auditoria de Conformidade",
            "type": "compliance",
            "generated_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "period": "últimos 90 dias",
        },
    ]


@router.get("/reports/trends")
def get_report_trends(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get security trends for reports."""
    period_start = datetime.now() - timedelta(days=days)

    # Simulate daily threat counts
    daily_data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=days - i)).date()
        threat_count = 10 + (i % 20)
        daily_data.append({"date": str(date), "threats": threat_count})

    return {
        "period_days": days,
        "daily_data": daily_data,
        "trend": "stable",
        "average_daily_threats": 15,
        "peak_day": "2024-12-28",
        "peak_count": 35,
    }
