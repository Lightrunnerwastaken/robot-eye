from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from backend.models import ContentUnit, Review

EASE_INTERVALS = {
    1: timedelta(minutes=10),
    2: timedelta(days=1),
    3: timedelta(days=2),
    4: timedelta(days=4),
    5: timedelta(days=7),
}


def schedule_review(content: ContentUnit, ease: int) -> Review:
    now = datetime.utcnow()
    next_due = now + EASE_INTERVALS.get(ease, timedelta(days=1))
    review = Review(content_id=content.id, ease=ease, next_due=next_due, updated_at=now)
    return review


def update_review(review: Review, ease: int) -> Review:
    now = datetime.utcnow()
    review.ease = ease
    review.next_due = now + EASE_INTERVALS.get(ease, timedelta(days=1))
    review.updated_at = now
    return review


def due_reviews(session: Session, limit: int = 20) -> list[Review]:
    return (
        session.query(Review)
        .filter(Review.next_due <= datetime.utcnow())
        .order_by(Review.next_due.asc())
        .limit(limit)
        .all()
    )
