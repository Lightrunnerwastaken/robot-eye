from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DifficultyEnum(str, Enum):
    """Valid difficulty levels for learning goals."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GoalBase(BaseModel):
    subject: str = Field(..., max_length=200, min_length=1)
    topic: str = Field(..., max_length=200, min_length=1)
    exam_date: date
    difficulty: DifficultyEnum
    notes: Optional[str] = None

    @field_validator("exam_date")
    @classmethod
    def validate_exam_date(cls, v: date) -> date:
        """Ensure exam date is not in the past."""
        from datetime import date as date_class
        today = date_class.today()
        if v < today:
            raise ValueError("Exam date cannot be in the past")
        return v


class GoalCreate(GoalBase):
    pass


class GoalRead(GoalBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
