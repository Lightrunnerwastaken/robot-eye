from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.database import session_scope
from backend.services import content_gen, planner

router = APIRouter(prefix="/generate", tags=["generate"])


def get_session():
    with session_scope() as session:
        yield session


@router.post("/plan", response_model=list[schemas.PlanBlockRead])
def generate_plan(payload: schemas.PlanGenerateRequest, session: Session = Depends(get_session)):
    goal = session.get(models.Goal, payload.goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    blocks = planner.generate_plan(session, goal, payload.start_date)
    session.flush()
    session.refresh(goal)
    return blocks


@router.post("/content", response_model=list[schemas.ContentUnitRead])
def generate_content(goal_id: int, session: Session = Depends(get_session)):
    goal = session.get(models.Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    generated = content_gen.generate_content(session, goal)
    return [*generated.flashcards, *generated.questions]


@router.post("/expand/explain", response_model=schemas.ContentUnitRead)
def expand_content(content_id: int, session: Session = Depends(get_session)):
    content = session.get(models.ContentUnit, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    updated = content_gen.expand_content(session, content)
    return updated
