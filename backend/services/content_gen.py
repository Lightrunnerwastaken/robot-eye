from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.models import ContentUnit, Goal
from backend.services.llm_provider import provider
from backend.services.review import schedule_review


@dataclass
class GeneratedContent:
    flashcards: list[ContentUnit]
    questions: list[ContentUnit]


def generate_content(session: Session, goal: Goal) -> GeneratedContent:
    """Create demo flashcards and questions for a goal."""

    templates = [
        ("flashcard", "remember", "Fasse das Kernthema zusammen."),
        ("question", "understand", "Erkläre das Konzept in eigenen Worten."),
        ("question", "analyze", "Analysiere eine typische Prüfungsfrage."),
    ]

    flashcards: list[ContentUnit] = []
    questions: list[ContentUnit] = []

    for type_, bloom, instruction in templates:
        prompt = _build_prompt(goal, bloom, instruction)
        completion = provider.complete(prompt)

        content = ContentUnit(
            goal_id=goal.id,
            type=type_,
            bloom=bloom,
            prompt=prompt,
            answer=completion.completion,
        )
        session.add(content)
        session.flush()

        review = schedule_review(content, ease=3)
        session.add(review)
        session.flush()

        if type_ == "flashcard":
            flashcards.append(content)
        else:
            questions.append(content)

    return GeneratedContent(flashcards=flashcards, questions=questions)


def create_micro_drill(session: Session, content: ContentUnit) -> ContentUnit:
    prompt = (
        "Erstelle einen Micro-Drill mit drei kurzen Aufgaben, die das Verständnis "
        f"des folgenden Inhalts vertiefen:\n\n{content.answer}"
    )
    completion = provider.complete(prompt)
    drill = ContentUnit(
        goal_id=content.goal_id,
        type="drill",
        bloom="apply",
        prompt=prompt,
        answer=completion.completion,
    )
    session.add(drill)
    session.flush()

    review = schedule_review(drill, ease=2)
    session.add(review)
    session.flush()
    return drill


def expand_content(session: Session, content: ContentUnit) -> ContentUnit:
    prompt = (
        f"Erweitere den Lerninhalt (Bloom: {content.bloom}) mit einer tieferen Erklärung "
        f"und einem Micro-Drill.\n\n{content.answer}"
    )
    completion = provider.complete(prompt)
    content.answer = completion.completion
    session.add(content)
    session.flush()
    return content


def _build_prompt(goal: Goal, bloom: str, instruction: str) -> str:
    return (
        f"Fach: {goal.subject}\nThema: {goal.topic}\nPrüfungsdatum: {goal.exam_date}\n"
        f"Bloom-Level: {bloom}\nAufgabe: {instruction}"
    )
