from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.content import ContentUnit
    from backend.models.goal import Goal


class PlanStep(Base):
    __tablename__ = "plan_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_id: Mapped[int] = mapped_column(ForeignKey("plan_blocks.id", ondelete="CASCADE"))
    content_id: Mapped[Optional[int]] = mapped_column(ForeignKey("content_units.id"), nullable=True)
    description: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[dict] = mapped_column(JSON, default=dict)

    block: Mapped["PlanBlock"] = relationship(back_populates="steps")
    content: Mapped[Optional["ContentUnit"]] = relationship()


class PlanBlock(Base):
    __tablename__ = "plan_blocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(Date, nullable=False)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    goal: Mapped["Goal"] = relationship(back_populates="plan_blocks")
    steps: Mapped[List[PlanStep]] = relationship(
        back_populates="block", cascade="all, delete-orphan", order_by="PlanStep.id"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"PlanBlock(id={self.id}, goal_id={self.goal_id}, date={self.date})"
