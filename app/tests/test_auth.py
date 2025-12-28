"""Authentication tests."""

import pytest
from fastapi import status


class TestAuthentication:
    """Authentication endpoint tests."""

    def test_register_user(self, client):
        """Test user registration."""
        response = client.post(
            "/api/v1/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "SecurePass123!",
                "full_name": "New User",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "password_hash" not in data

    def test_register_user_duplicate_username(self, client, test_user):
        """Test registration with duplicate username."""
        response = client.post(
            "/api/v1/register",
            json={
                "username": "testuser",
                "email": "different@example.com",
                "password": "SecurePass123!",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/token",
            data={"username": "testuser", "password": "testpassword123"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_password(self, client, test_user):
        """Test login with wrong password."""
        response = client.post(
            "/api/v1/token",
            data={"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, client, auth_token):
        """Test getting current user info."""
        response = client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
