from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ContentTypeEnum(str, Enum):
    """Valid content types."""
    FLASHCARD = "flashcard"
    QUESTION = "question"
    DRILL = "drill"


class BloomLevelEnum(str, Enum):
    """Bloom's taxonomy cognitive levels."""
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class ContentUnitBase(BaseModel):
    goal_id: int
    type: ContentTypeEnum
    bloom: BloomLevelEnum
    prompt: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)


class ContentUnitCreate(ContentUnitBase):
    pass


class ContentUnitRead(ContentUnitBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
