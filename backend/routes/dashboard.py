from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import session_scope
from backend.schemas import DashboardRead
from backend.services.dashboard import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def get_session():
    with session_scope() as session:
        yield session


@router.get("/", response_model=DashboardRead)
def read_dashboard(session: Session = Depends(get_session)):
    return get_dashboard(session)
