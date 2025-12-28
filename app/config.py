"""Application configuration."""

from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    APP_NAME: str = "SecureGuard Security Monitoring System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/secureapps")
    SQLALCHEMY_DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/secureapps")
    SQLALCHEMY_ECHO: bool = False

    # JWT
    SECRET_KEY: str = Field(default="your-super-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@secureapps.com"

    # Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # Slack
    SLACK_WEBHOOK_URL: str = ""
    SLACK_BOT_TOKEN: str = ""

    # VirusTotal
    VIRUSTOTAL_API_KEY: str = ""

    # Shodan
    SHODAN_API_KEY: str = ""

    # Elasticsearch
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_USERNAME: str = "elastic"
    ELASTICSEARCH_PASSWORD: str = "changeme"

    # Prometheus
    PROMETHEUS_ENABLED: bool = True
    PROMETHEUS_PORT: int = 8001

    # CORS
    ALLOWED_ORIGINS: List[str] = Field(default=["http://localhost:3000", "https://localhost:3000"])

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
