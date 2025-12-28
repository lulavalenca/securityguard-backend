"""Threat detection tests."""

import pytest
from fastapi import status
from app.models.threat import ThreatType, ThreatSeverity


class TestThreats:
    """Threat endpoints tests."""

    def test_list_threats(self, client, auth_token):
        """Test listing threats."""
        response = client.get(
            "/api/v1/threats",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_create_threat(self, client, auth_token):
        """Test creating a threat."""
        response = client.post(
            "/api/v1/threats",
            json={
                "threat_type": "malware",
                "severity": "critical",
                "source_ip": "192.168.1.100",
                "destination_ip": "192.168.1.1",
                "description": "Malware detected in network traffic",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["threat_type"] == "malware"
        assert data["severity"] == "critical"
        assert data["status"] == "active"

    def test_get_threat(self, client, auth_token, db):
        """Test getting a specific threat."""
        from app.models.threat import Threat

        threat = Threat(
            threat_type=ThreatType.BRUTE_FORCE,
            severity=ThreatSeverity.HIGH,
            source_ip="192.168.1.50",
            description="Brute force attempt detected",
        )
        db.add(threat)
        db.commit()

        response = client.get(
            f"/api/v1/threats/{threat.id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == threat.id
        assert data["threat_type"] == "brute_force"

    def test_update_threat(self, client, auth_token, db):
        """Test updating threat status."""
        from app.models.threat import Threat, ThreatStatus

        threat = Threat(
            threat_type=ThreatType.MALWARE,
            severity=ThreatSeverity.CRITICAL,
            source_ip="10.0.0.5",
            description="Test malware",
        )
        db.add(threat)
        db.commit()

        response = client.patch(
            f"/api/v1/threats/{threat.id}",
            json={"status": "mitigated"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "mitigated"
