from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.database import session_scope
from backend.models.goal import difficulties as allowed_difficulties

router = APIRouter(prefix="/goals", tags=["goals"])


def get_session():
    with session_scope() as session:
        yield session


@router.get("/", response_model=list[schemas.GoalRead])
def list_goals(session: Session = Depends(get_session)):
    return session.query(models.Goal).order_by(models.Goal.created_at.desc()).all()


@router.post("/", response_model=schemas.GoalRead)
def create_goal(goal: schemas.GoalCreate, session: Session = Depends(get_session)):
    if goal.difficulty not in allowed_difficulties:
        raise HTTPException(status_code=400, detail="Invalid difficulty value")
    db_goal = models.Goal(**goal.dict())
    session.add(db_goal)
    session.flush()
    return db_goal


@router.get("/{goal_id}", response_model=schemas.GoalRead)
def get_goal(goal_id: int, session: Session = Depends(get_session)):
    goal = session.get(models.Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal
