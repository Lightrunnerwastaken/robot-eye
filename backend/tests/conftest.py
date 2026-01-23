"""Test fixtures and configuration for pytest."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Import models to register them with Base
from backend import models  # noqa: F401
from backend.database import Base
from backend.dependencies import get_session
from backend.main import app


@pytest.fixture(scope="function")
def test_db():
    """Create a test database."""
    # SQLite with check_same_thread=False for testing
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    
    session = TestSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db: Session):
    """Create a test client with test database."""
    def override_get_session():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_session] = override_get_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
