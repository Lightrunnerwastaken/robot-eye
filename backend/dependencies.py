"""Centralized FastAPI dependencies."""
from __future__ import annotations

from typing import Generator

from sqlalchemy.orm import Session

from backend.database import SessionLocal


def get_session() -> Generator[Session, None, None]:
    """Provide database session for dependency injection."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
