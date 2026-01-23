from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.dependencies import get_session
from backend.logging_config import logger
from backend.schemas import DashboardRead
from backend.services.dashboard import get_dashboard

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardRead)
def read_dashboard(session: Session = Depends(get_session)):
    """Get dashboard data with stats and progress."""
    logger.info("Fetching dashboard data")
    try:
        dashboard = get_dashboard(session)
        logger.info("Dashboard data retrieved successfully")
        return dashboard
    except Exception as e:
        logger.error(f"Failed to fetch dashboard: {e}")
        raise
