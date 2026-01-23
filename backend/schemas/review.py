from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .content import ContentUnitRead


class ReviewBase(BaseModel):
    content_id: int
    ease: int = Field(..., ge=1, le=5, description="Ease rating from 1 (hard) to 5 (easy)")


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    ease: int = Field(..., ge=1, le=5, description="Ease rating from 1 (hard) to 5 (easy)")


class ReviewRead(ReviewBase):
    id: int
    next_due: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ReviewFeedback(BaseModel):
    review: ReviewRead
    expanded_content: Optional[ContentUnitRead] = None
    micro_drill: Optional[ContentUnitRead] = None
