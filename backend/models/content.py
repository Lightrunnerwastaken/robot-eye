from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

content_types = ("flashcard", "question", "drill")
bloom_levels = ("remember", "understand", "apply", "analyze", "evaluate", "create")


class ContentUnit(Base):
    __tablename__ = "content_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(Enum(*content_types, name="content_type"), nullable=False)
    bloom: Mapped[str] = mapped_column(Enum(*bloom_levels, name="bloom_level"), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    goal: Mapped["Goal"] = relationship(back_populates="contents")
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="content", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"ContentUnit(id={self.id}, type={self.type}, bloom={self.bloom})"
