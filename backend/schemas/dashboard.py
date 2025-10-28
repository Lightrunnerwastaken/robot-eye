from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class DashboardBlock(BaseModel):
    date: date
    tasks: list[dict]


class DashboardRead(BaseModel):
    goals: int
    due_reviews: int
    completion_rate: float
    today_blocks: list[DashboardBlock]
