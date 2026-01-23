from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GoalBase(BaseModel):
    subject: str = Field(..., max_length=200)
    topic: str = Field(..., max_length=200)
    exam_date: date
    difficulty: str
    notes: Optional[str] = None


class GoalCreate(GoalBase):
    pass


class GoalRead(GoalBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
