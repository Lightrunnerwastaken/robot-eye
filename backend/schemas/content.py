from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ContentUnitBase(BaseModel):
    goal_id: int
    type: str
    bloom: str
    prompt: str
    answer: str


class ContentUnitCreate(ContentUnitBase):
    pass


class ContentUnitRead(ContentUnitBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
