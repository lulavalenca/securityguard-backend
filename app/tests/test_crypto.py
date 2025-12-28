"""Cryptography tests."""

import pytest
from fastapi import status


class TestCryptography:
    """Cryptography endpoints tests."""

    def test_hash_generation(self, client, auth_token):
        """Test hash generation."""
        response = client.post(
            "/api/v1/crypto/hash",
            json={
                "text": "test_password_123",
                "algorithms": ["sha256", "sha512", "md5"],
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "sha256" in data
        assert "sha512" in data
        assert "md5" in data
        assert len(data["sha256"]) == 64  # SHA-256 hex length
        assert len(data["sha512"]) == 128  # SHA-512 hex length

    def test_aes_encrypt(self, client, auth_token):
        """Test AES encryption."""
        response = client.post(
            "/api/v1/crypto/aes/encrypt",
            json={
                "mode": "CBC",
                "key_hex": "0" * 32,  # 128-bit key in hex
                "plaintext": "Secret message",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "ciphertext" in data
        assert "iv" in data

    def test_aes_decrypt(self, client, auth_token):
        """Test AES decryption."""
        # First encrypt
        encrypt_response = client.post(
            "/api/v1/crypto/aes/encrypt",
            json={
                "mode": "CBC",
                "key_hex": "0" * 32,
                "plaintext": "Secret message",
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        ciphertext = encrypt_response.json()["ciphertext"]

        # Then decrypt
        decrypt_response = client.post(
            "/api/v1/crypto/aes/decrypt",
            json={
                "mode": "CBC",
                "key_hex": "0" * 32,
                "ciphertext_b64": ciphertext,
            },
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert decrypt_response.status_code == status.HTTP_200_OK
        data = decrypt_response.json()
        assert "plaintext" in data
