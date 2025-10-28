from __future__ import annotations

from datetime import date, timedelta
from typing import Iterable

from sqlalchemy.orm import Session

from backend.models import Goal, PlanBlock, PlanStep

BLOOM_SEQUENCE = [
    ("remember", "Erinnerungs-Flashcard"),
    ("understand", "Verständnisfrage"),
    ("apply", "Anwendungsaufgabe"),
    ("analyze", "Analyseaufgabe"),
    ("evaluate", "Bewertungsreflexion"),
    ("create", "Kreativprojekt"),
]


def generate_plan(session: Session, goal: Goal, start_date: date | None = None) -> list[PlanBlock]:
    """Generate plan blocks from today until the exam date."""

    session.query(PlanBlock).filter(PlanBlock.goal_id == goal.id).delete()

    start = start_date or date.today()
    total_days = max((goal.exam_date - start).days + 1, 1)
    sequence = list(_cycle_bloom_sequence(total_days))

    blocks: list[PlanBlock] = []
    for offset, (bloom, description) in enumerate(sequence):
        current_date = start + timedelta(days=offset)
        block = PlanBlock(goal_id=goal.id, date=current_date, meta={"focus": bloom})
        session.add(block)
        session.flush()

        step = PlanStep(
            block_id=block.id,
            content_id=None,
            description={
                "title": description,
                "bloom": bloom,
                "details": f"Arbeite an '{goal.topic}' mit Schwerpunkt {bloom}.",
            },
            status={"done": False},
        )
        session.add(step)
        session.flush()
        blocks.append(block)

    return blocks


def _cycle_bloom_sequence(length: int) -> Iterable[tuple[str, str]]:
    idx = 0
    while idx < length:
        yield BLOOM_SEQUENCE[idx % len(BLOOM_SEQUENCE)]
        idx += 1
