from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_session
from backend.exceptions import ResourceNotFoundError
from backend.logging_config import logger
from backend.services import content_gen, planner

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("/plan", response_model=list[schemas.PlanBlockRead])
def generate_plan(payload: schemas.PlanGenerateRequest, session: Session = Depends(get_session)):
    """Generate a learning plan for a goal."""
    logger.info(f"Generating plan for goal {payload.goal_id}")
    
    goal = session.get(models.Goal, payload.goal_id)
    if not goal:
        raise ResourceNotFoundError("Goal", payload.goal_id)

    try:
        blocks = planner.generate_plan(session, goal, payload.start_date)
        session.commit()
        session.refresh(goal)
        logger.info(f"Generated {len(blocks)} plan blocks for goal {payload.goal_id}")
        return blocks
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to generate plan: {e}")
        raise


@router.post("/content", response_model=list[schemas.ContentUnitRead])
def generate_content(goal_id: int, session: Session = Depends(get_session)):
    """Generate learning content for a goal."""
    logger.info(f"Generating content for goal {goal_id}")
    
    goal = session.get(models.Goal, goal_id)
    if not goal:
        raise ResourceNotFoundError("Goal", goal_id)
    
    try:
        generated = content_gen.generate_content(session, goal)
        logger.info(f"Generated {len(generated.flashcards)} flashcards and {len(generated.questions)} questions")
        return [*generated.flashcards, *generated.questions]
    except Exception as e:
        logger.error(f"Failed to generate content: {e}")
        raise


@router.post("/expand/explain", response_model=schemas.ContentUnitRead)
def expand_content(content_id: int, session: Session = Depends(get_session)):
    """Expand/explain a content unit in more detail."""
    logger.info(f"Expanding content {content_id}")
    
    content = session.get(models.ContentUnit, content_id)
    if not content:
        raise ResourceNotFoundError("Content", content_id)
    
    try:
        updated = content_gen.expand_content(session, content)
        logger.info(f"Expanded content {content_id}")
        return updated
    except Exception as e:
        logger.error(f"Failed to expand content: {e}")
        raise
