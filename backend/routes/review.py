from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.database import session_scope
from backend.services import content_gen
from backend.services import review as review_service

router = APIRouter(prefix="/review", tags=["review"])


def get_session():
    with session_scope() as session:
        yield session


@router.post("/", response_model=schemas.ReviewRead)
def create_review(payload: schemas.ReviewCreate, session: Session = Depends(get_session)):
    content = session.get(models.ContentUnit, payload.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    review = review_service.schedule_review(content, payload.ease)
    session.add(review)
    session.flush()
    return review


@router.put("/{review_id}", response_model=schemas.ReviewFeedback)
def update_review(review_id: int, payload: schemas.ReviewUpdate, session: Session = Depends(get_session)):
    review = session.get(models.Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    updated = review_service.update_review(review, payload.ease)
    session.add(updated)
    session.flush()

    expanded = None
    drill = None
    if payload.ease == 1:
        content = session.get(models.ContentUnit, review.content_id)
        if content is not None:
            expanded = content_gen.expand_content(session, content)
            drill = content_gen.create_micro_drill(session, content)

    return schemas.ReviewFeedback(
        review=updated,
        expanded_content=expanded,
        micro_drill=drill,
    )


@router.get("/due", response_model=list[schemas.ReviewRead])
def due_reviews(limit: int = 20, session: Session = Depends(get_session)):
    return review_service.due_reviews(session, limit=limit)
