"""Data encryption utilities."""

from cryptography.fernet import Fernet
from app.config import get_settings

settings = get_settings()

# Em produção, usar chave do ambiente
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)


def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data."""
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()
