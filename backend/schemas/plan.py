from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PlanStepRead(BaseModel):
    id: int
    content_id: Optional[int]
    description: dict[str, Any]
    status: dict[str, Any]
    
    model_config = ConfigDict(from_attributes=True)


class PlanBlockRead(BaseModel):
    id: int
    goal_id: int
    date: date
    meta: dict[str, Any]
    created_at: datetime
    steps: list[PlanStepRead]
    
    model_config = ConfigDict(from_attributes=True)


class PlanGenerateRequest(BaseModel):
    goal_id: int
    start_date: Optional[date] = None
