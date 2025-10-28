from __future__ import annotations

from datetime import date, timedelta

from backend.database import Base, engine, session_scope
from backend.models import Goal
from backend.services import content_gen, planner

Base.metadata.create_all(bind=engine)


def seed():
    with session_scope() as session:
        goal = Goal(
            subject="Neurowissenschaften",
            topic="Synaptische Plastizität",
            exam_date=date.today() + timedelta(days=14),
            difficulty="medium",
            notes="Vorbereitung für die Neurophysiologie-Klausur",
        )
        session.add(goal)
        session.flush()

        content_gen.generate_content(session, goal)
        planner.generate_plan(session, goal)

        print("Seed data created: goal", goal.id)


if __name__ == "__main__":
    seed()
