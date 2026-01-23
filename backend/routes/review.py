from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.dependencies import get_session
from backend.exceptions import ResourceNotFoundError, ValidationError
from backend.logging_config import logger
from backend.services import content_gen
from backend.services import review as review_service

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/", response_model=schemas.ReviewRead)
def create_review(payload: schemas.ReviewCreate, session: Session = Depends(get_session)):
    """Create a new review for a content unit."""
    logger.info(f"Creating review for content {payload.content_id} with ease {payload.ease}")
    
    content = session.get(models.ContentUnit, payload.content_id)
    if not content:
        raise ResourceNotFoundError("Content", payload.content_id)
    
    try:
        review = review_service.schedule_review(content, payload.ease)
        session.add(review)
        session.commit()
        session.refresh(review)
        logger.info(f"Created review with id {review.id}")
        return review
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create review: {e}")
        raise


@router.put("/{review_id}", response_model=schemas.ReviewFeedback)
def update_review(review_id: int, payload: schemas.ReviewUpdate, session: Session = Depends(get_session)):
    """Update a review and get feedback."""
    logger.info(f"Updating review {review_id} with ease {payload.ease}")
    
    review = session.get(models.Review, review_id)
    if not review:
        raise ResourceNotFoundError("Review", review_id)

    try:
        updated = review_service.update_review(review, payload.ease)
        session.add(updated)
        session.commit()

        expanded = None
        drill = None
        if payload.ease == 1:
            content = session.get(models.ContentUnit, review.content_id)
            if content is not None:
                expanded = content_gen.expand_content(session, content)
                drill = content_gen.create_micro_drill(session, content)

        logger.info(f"Updated review {review_id}")
        return schemas.ReviewFeedback(
            review=updated,
            expanded_content=expanded,
            micro_drill=drill,
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to update review: {e}")
        raise


@router.get("/due", response_model=list[schemas.ReviewRead])
def due_reviews(limit: int = 20, session: Session = Depends(get_session)):
    """Get list of reviews that are due."""
    logger.info(f"Fetching due reviews (limit={limit})")
    reviews = review_service.due_reviews(session, limit=limit)
    logger.info(f"Found {len(reviews)} due reviews")
    return reviews
