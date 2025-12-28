"""Port scanning and vulnerability scanning endpoints."""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field, IPvAnyAddress
from datetime import datetime

from app.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.vulnerability import Vulnerability, VulnerabilityStatus
from sqlalchemy.orm import Session

router = APIRouter()


class PortScanRequest(BaseModel):
    """Port scan request."""
    target: str = Field(..., description="IP address or hostname")
    port: int = Field(..., ge=1, le=65535, description="Port number")
    scan_type: str = Field(default="tcp", pattern="^(tcp|syn|udp|ack)$")


class PortRangeScanRequest(BaseModel):
    """Port range scan request."""
    target: str = Field(..., description="IP address or hostname")
    port_range: str = Field(
        default="common", pattern="^(common|web|db|ssh|all)$"
    )
    timing: str = Field(default="normal", pattern="^(slow|normal|fast|aggressive)$")


class VulnerabilityScanRequest(BaseModel):
    """Vulnerability scan request."""
    target: str = Field(..., description="IP address or hostname")
    scan_depth: str = Field(default="light", pattern="^(light|moderate|deep|full)$")


class PortScanResult(BaseModel):
    """Port scan result."""
    target: str
    port: int
    status: str  # open, closed, filtered
    service: str
    protocol: str
    timestamp: datetime


class VulnerabilityScanResult(BaseModel):
    """Vulnerability scan result."""
    target: str
    vulnerabilities_found: int
    critical: int
    high: int
    medium: int
    low: int
    scan_start: datetime
    scan_end: datetime


@router.post("/scanning/port", response_model=PortScanResult)
def scan_single_port(
    request: PortScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PortScanResult:
    """Scan a single port on target."""
    # Simulação de scan
    import random

    statuses = ["open", "closed", "filtered"]
    services = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL",
        5432: "PostgreSQL",
        27017: "MongoDB",
    }

    return PortScanResult(
        target=request.target,
        port=request.port,
        status=random.choice(statuses),
        service=services.get(request.port, "Unknown"),
        protocol=request.scan_type.upper(),
        timestamp=datetime.now(),
    )


@router.post("/scanning/port-range", response_model=List[PortScanResult])
def scan_port_range(
    request: PortRangeScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[PortScanResult]:
    """Scan port range on target."""
    import random

    port_ranges = {
        "common": [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 8080, 8443],
        "web": [80, 443, 8080, 8443],
        "db": [3306, 5432, 1433, 27017],
        "ssh": [22, 3389, 5900],
        "all": list(range(1, 1001)),
    }

    ports = port_ranges.get(request.port_range, port_ranges["common"])
    results = []

    for port in ports[:10]:  # Limitar a 10 resultados
        results.append(
            PortScanResult(
                target=request.target,
                port=port,
                status=random.choice(["open", "closed", "filtered"]),
                service=f"Service_{port}",
                protocol="TCP",
                timestamp=datetime.now(),
            )
        )

    return results


@router.post("/scanning/vulnerabilities", response_model=VulnerabilityScanResult)
def scan_vulnerabilities(
    request: VulnerabilityScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> VulnerabilityScanResult:
    """Scan target for vulnerabilities."""
    import random

    scan_start = datetime.now()

    # Simular criação de vulnerabilidades
    vuln_counts = {
        "light": {"critical": 0, "high": 1, "medium": 3, "low": 5},
        "moderate": {"critical": 1, "high": 3, "medium": 8, "low": 12},
        "deep": {"critical": 2, "high": 5, "medium": 15, "low": 20},
        "full": {"critical": 3, "high": 8, "medium": 20, "low": 30},
    }

    counts = vuln_counts.get(request.scan_depth, vuln_counts["light"])

    return VulnerabilityScanResult(
        target=request.target,
        vulnerabilities_found=sum(counts.values()),
        critical=counts["critical"],
        high=counts["high"],
        medium=counts["medium"],
        low=counts["low"],
        scan_start=scan_start,
        scan_end=datetime.now(),
    )


@router.get("/scanning/results/vulnerabilities", response_model=List[Dict[str, Any]])
def get_vulnerability_results(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get stored vulnerability scan results."""
    vulns = (
        db.query(Vulnerability)
        .order_by(Vulnerability.discovered_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id": v.id,
            "cve_id": v.cve_id,
            "title": v.title,
            "severity": v.severity,
            "cvss_score": float(v.cvss_score) if v.cvss_score else None,
            "affected_system": v.affected_system,
            "status": v.status.value,
            "discovered_at": v.discovered_at.isoformat(),
        }
        for v in vulns
    ]
