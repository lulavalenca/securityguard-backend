"""Database configuration and connection."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from typing import Generator

from app.config import get_settings

settings = get_settings()

# Create engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    poolclass=NullPool if settings.ENVIRONMENT == "test" else None,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
