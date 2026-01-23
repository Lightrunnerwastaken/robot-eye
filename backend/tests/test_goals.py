"""Unit tests for goal endpoints."""
from __future__ import annotations

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_create_goal_success(client: TestClient):
    """Test creating a goal successfully."""
    tomorrow = date.today() + timedelta(days=1)
    goal_data = {
        "subject": "Python Programming",
        "topic": "FastAPI Basics",
        "exam_date": tomorrow.isoformat(),
        "difficulty": "medium",
        "notes": "Focus on async patterns"
    }
    
    response = client.post("/goals/", json=goal_data)
    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == goal_data["subject"]
    assert data["topic"] == goal_data["topic"]
    assert data["difficulty"] == goal_data["difficulty"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.unit
def test_create_goal_past_exam_date(client: TestClient):
    """Test that creating a goal with past exam date fails."""
    yesterday = date.today() - timedelta(days=1)
    goal_data = {
        "subject": "Python Programming",
        "topic": "FastAPI Basics",
        "exam_date": yesterday.isoformat(),
        "difficulty": "medium",
    }
    
    response = client.post("/goals/", json=goal_data)
    assert response.status_code == 422


@pytest.mark.unit
def test_create_goal_invalid_difficulty(client: TestClient):
    """Test that creating a goal with invalid difficulty fails."""
    tomorrow = date.today() + timedelta(days=1)
    goal_data = {
        "subject": "Python Programming",
        "topic": "FastAPI Basics",
        "exam_date": tomorrow.isoformat(),
        "difficulty": "impossible",
    }
    
    response = client.post("/goals/", json=goal_data)
    assert response.status_code == 422


@pytest.mark.unit
def test_list_goals(client: TestClient):
    """Test listing goals."""
    # Create a goal first
    tomorrow = date.today() + timedelta(days=1)
    goal_data = {
        "subject": "Math",
        "topic": "Calculus",
        "exam_date": tomorrow.isoformat(),
        "difficulty": "hard",
    }
    client.post("/goals/", json=goal_data)
    
    # List goals
    response = client.get("/goals/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["subject"] == "Math"


@pytest.mark.unit
def test_get_goal_by_id(client: TestClient):
    """Test getting a specific goal by ID."""
    tomorrow = date.today() + timedelta(days=1)
    goal_data = {
        "subject": "Physics",
        "topic": "Quantum Mechanics",
        "exam_date": tomorrow.isoformat(),
        "difficulty": "hard",
    }
    create_response = client.post("/goals/", json=goal_data)
    goal_id = create_response.json()["id"]
    
    response = client.get(f"/goals/{goal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == goal_id
    assert data["subject"] == "Physics"


@pytest.mark.unit
def test_get_nonexistent_goal(client: TestClient):
    """Test getting a goal that doesn't exist."""
    response = client.get("/goals/99999")
    assert response.status_code == 404
