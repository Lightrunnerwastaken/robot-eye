from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class GoalBase(BaseModel):
    subject: str = Field(..., max_length=200)
    topic: str = Field(..., max_length=200)
    exam_date: date
    difficulty: str
    notes: str | None = None


class GoalCreate(GoalBase):
    pass


class GoalRead(GoalBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
