from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from .content import ContentUnitRead


class ReviewBase(BaseModel):
    content_id: int
    ease: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    ease: int


class ReviewRead(ReviewBase):
    id: int
    next_due: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ReviewFeedback(BaseModel):
    review: ReviewRead
    expanded_content: ContentUnitRead | None = None
    micro_drill: ContentUnitRead | None = None
