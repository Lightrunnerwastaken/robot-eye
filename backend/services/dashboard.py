from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.orm import Session

from backend.models import Goal, PlanBlock, Review


def get_dashboard(session: Session) -> dict:
    today = date.today()
    goals = session.query(Goal).count()
    due = session.query(Review).filter(Review.next_due <= datetime.utcnow()).count()

    today_blocks = (
        session.query(PlanBlock)
        .filter(PlanBlock.date == today)
        .order_by(PlanBlock.goal_id.asc())
        .all()
    )

    total_steps = 0
    completed = 0
    blocks_payload = []
    for block in today_blocks:
        steps_payload = []
        for step in block.steps:
            done = bool(step.status.get("done"))
            total_steps += 1
            completed += int(done)
            steps_payload.append(
                {
                    "id": step.id,
                    "description": step.description,
                    "status": step.status,
                }
            )
        blocks_payload.append({"date": block.date, "tasks": steps_payload, "goal_id": block.goal_id})

    completion_rate = (completed / total_steps) * 100 if total_steps else 0.0

    return {
        "goals": goals,
        "due_reviews": due,
        "completion_rate": round(completion_rate, 1),
        "today_blocks": blocks_payload,
    }
