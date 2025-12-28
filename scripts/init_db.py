#!/usr/bin/env python
"""Initialize database with schema and sample data."""

import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

sys.path.insert(0, '/app')

from app.database import engine, SessionLocal, Base
from app.models import (
    User, Threat, Log, NetworkTraffic, Vulnerability,
    SSLCertificate, SecurityPolicy
)
from app.models.user import UserRole
from app.models.threat import ThreatType, ThreatSeverity, ThreatStatus
from app.models.vulnerability import VulnerabilityStatus
from app.security.password_hasher import hash_password


def init_database():
    """Create tables and insert sample data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")

    db = SessionLocal()
    try:
        # Check if admin exists
        admin_exists = db.query(User).filter(User.username == "admin").first()
        if not admin_exists:
            print("Creating admin user...")
            admin = User(
                username="admin",
                email="admin@secureapps.com",
                password_hash=hash_password("admin123"),
                full_name="Administrator",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin)

            analyst = User(
                username="analyst",
                email="analyst@secureapps.com",
                password_hash=hash_password("analyst123"),
                full_name="Security Analyst",
                role=UserRole.ANALYST,
                is_active=True,
            )
            db.add(analyst)

            viewer = User(
                username="viewer",
                email="viewer@secureapps.com",
                password_hash=hash_password("viewer123"),
                full_name="Viewer User",
                role=UserRole.VIEWER,
                is_active=True,
            )
            db.add(viewer)
            db.commit()
            print("✓ Users created successfully")
        
        # Create sample threats
        threats_count = db.query(Threat).count()
        if threats_count == 0:
            print("Creating sample threats...")
            sample_threats = [
                Threat(
                    threat_type=ThreatType.MALWARE,
                    severity=ThreatSeverity.CRITICAL,
                    source_ip="203.0.113.45",
                    destination_ip="192.168.1.10",
                    description="Malware detection - WannaCry variant",
                    status=ThreatStatus.ACTIVE,
                    details={"malware_family": "WannaCry", "detected_at": "2024-12-28T20:00:00Z"},
                ),
                Threat(
                    threat_type=ThreatType.BRUTE_FORCE,
                    severity=ThreatSeverity.HIGH,
                    source_ip="198.51.100.22",
                    destination_ip="192.168.1.50",
                    description="Brute force attack on SSH port",
                    status=ThreatStatus.ACTIVE,
                    details={"port": 22, "attempts": 245},
                ),
                Threat(
                    threat_type=ThreatType.SQL_INJECTION,
                    severity=ThreatSeverity.CRITICAL,
                    source_ip="192.0.2.88",
                    destination_ip="192.168.1.100",
                    description="SQL Injection attempt detected",
                    status=ThreatStatus.MITIGATED,
                    details={"endpoint": "/api/users", "payload": "OR 1=1"},
                ),
            ]
            for threat in sample_threats:
                db.add(threat)
            db.commit()
            print("✓ Sample threats created successfully")
        
        # Create sample network traffic
        traffic_count = db.query(NetworkTraffic).count()
        if traffic_count == 0:
            print("Creating sample network traffic...")
            sample_traffic = [
                NetworkTraffic(
                    source_ip="192.168.1.50",
                    destination_ip="8.8.8.8",
                    source_port=54321,
                    destination_port=443,
                    protocol="TCP",
                    packet_count=450,
                    bytes_sent=125000,
                    bytes_received=89500,
                    status="normal",
                ),
                NetworkTraffic(
                    source_ip="192.168.1.100",
                    destination_ip="203.0.113.99",
                    source_port=49152,
                    destination_port=22,
                    protocol="TCP",
                    packet_count=1200,
                    bytes_sent=48000,
                    bytes_received=125000,
                    status="suspicious",
                ),
            ]
            for traffic in sample_traffic:
                db.add(traffic)
            db.commit()
            print("✓ Sample network traffic created successfully")
        
        # Create sample vulnerabilities
        vuln_count = db.query(Vulnerability).count()
        if vuln_count == 0:
            print("Creating sample vulnerabilities...")
            sample_vulns = [
                Vulnerability(
                    cve_id="CVE-2024-1234",
                    title="Remote Code Execution in API",
                    description="Unauthenticated RCE vulnerability found in REST API endpoint",
                    cvss_score=9.8,
                    severity="critical",
                    affected_system="Production Web Server",
                    remediation="Update to version 2.5.0 or apply security patch",
                    discovered_at=datetime.now() - timedelta(days=5),
                    status=VulnerabilityStatus.OPEN,
                ),
                Vulnerability(
                    cve_id="CVE-2024-5678",
                    title="SQL Injection in User Login",
                    description="SQL injection vulnerability in authentication module",
                    cvss_score=8.6,
                    severity="high",
                    affected_system="Application Database",
                    remediation="Use parameterized queries",
                    discovered_at=datetime.now() - timedelta(days=3),
                    status=VulnerabilityStatus.IN_PROGRESS,
                    remediated_at=None,
                ),
            ]
            for vuln in sample_vulns:
                db.add(vuln)
            db.commit()
            print("✓ Sample vulnerabilities created successfully")
        
        print("\n✓ Database initialization completed successfully!")
        print("\nDefault credentials:")
        print("  Admin:    admin / admin123")
        print("  Analyst:  analyst / analyst123")
        print("  Viewer:   viewer / viewer123")
        
    except Exception as e:
        print(f"✗ Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
