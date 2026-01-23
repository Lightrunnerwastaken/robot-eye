from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_session
from backend.exceptions import ResourceNotFoundError, ValidationError
from backend.logging_config import logger
from backend.models.goal import difficulties as allowed_difficulties

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/", response_model=list[schemas.GoalRead])
def list_goals(session: Session = Depends(get_session)):
    """List all learning goals."""
    logger.info("Fetching all goals")
    goals = session.query(models.Goal).order_by(models.Goal.created_at.desc()).all()
    logger.info(f"Found {len(goals)} goals")
    return goals


@router.post("/", response_model=schemas.GoalRead)
def create_goal(goal: schemas.GoalCreate, session: Session = Depends(get_session)):
    """Create a new learning goal."""
    logger.info(f"Creating goal: {goal.title}")
    
    if goal.difficulty not in allowed_difficulties:
        raise ValidationError(
            f"Invalid difficulty '{goal.difficulty}'. Must be one of: {', '.join(allowed_difficulties)}"
        )
    
    try:
        db_goal = models.Goal(**goal.model_dump())
        session.add(db_goal)
        session.commit()
        session.refresh(db_goal)
        logger.info(f"Created goal with id {db_goal.id}")
        return db_goal
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create goal: {e}")
        raise


@router.get("/{goal_id}", response_model=schemas.GoalRead)
def get_goal(goal_id: int, session: Session = Depends(get_session)):
    """Get a specific goal by ID."""
    logger.info(f"Fetching goal {goal_id}")
    goal = session.get(models.Goal, goal_id)
    if not goal:
        raise ResourceNotFoundError("Goal", goal_id)
    return goal
