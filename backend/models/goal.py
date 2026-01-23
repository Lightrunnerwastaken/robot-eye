from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


difficulties = ("easy", "medium", "hard")


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    subject: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    exam_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    difficulty: Mapped[str] = mapped_column(Enum(*difficulties, name="difficulty"), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    contents: Mapped[list["ContentUnit"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )
    plan_blocks: Mapped[list["PlanBlock"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"Goal(id={self.id}, subject={self.subject!r}, topic={self.topic!r})"
