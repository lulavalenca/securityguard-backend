"""Security endpoints tests."""

import pytest
from fastapi import status


class TestSecurityDashboard:
    """Security dashboard tests."""

    def test_get_dashboard(self, client, auth_token):
        """Test getting security dashboard."""
        response = client.get(
            "/api/v1/security/dashboard",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "system_health" in data
        assert "threats_detected" in data
        assert "critical_threats" in data

    def test_threats_by_type(self, client, auth_token):
        """Test threats grouped by type."""
        response = client.get(
            "/api/v1/security/threats/by-type",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, dict)

    def test_network_activity(self, client, auth_token):
        """Test network activity metrics."""
        response = client.get(
            "/api/v1/security/network-activity?hours=24",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_packets" in data
        assert "total_bytes_sent" in data
