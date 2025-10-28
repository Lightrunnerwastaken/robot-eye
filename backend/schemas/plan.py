from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class PlanStepRead(BaseModel):
    id: int
    content_id: int | None
    description: dict[str, Any]
    status: dict[str, Any]

    class Config:
        orm_mode = True


class PlanBlockRead(BaseModel):
    id: int
    goal_id: int
    date: date
    meta: dict[str, Any]
    created_at: datetime
    steps: list[PlanStepRead]

    class Config:
        orm_mode = True


class PlanGenerateRequest(BaseModel):
    goal_id: int
    start_date: date | None = None
