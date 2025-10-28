from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_id: Mapped[int] = mapped_column(ForeignKey("content_units.id", ondelete="CASCADE"))
    ease: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    next_due: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    content: Mapped["ContentUnit"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Review(id={self.id}, content_id={self.content_id}, ease={self.ease})"
