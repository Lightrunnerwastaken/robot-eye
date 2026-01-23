# NeuroLearn API Documentation

## Overview

NeuroLearn is a learning platform API that provides endpoints for managing learning goals, generating content, scheduling reviews, and tracking progress.

**Base URL**: `http://localhost:8000` (development)

**API Version**: 0.1.0

## Authentication

Currently, the API does not require authentication. Authentication will be added in a future release.

## Endpoints

### Health Check

#### `GET /health`

Check API health status.

**Response**:
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

### Goals

#### `GET /goals/`

List all learning goals.

**Response**: Array of Goal objects

**Example**:
```json
[
  {
    "id": 1,
    "subject": "Python Programming",
    "topic": "FastAPI Basics",
    "exam_date": "2026-03-15",
    "difficulty": "medium",
    "notes": "Focus on async patterns",
    "created_at": "2026-01-23T10:00:00"
  }
]
```

#### `POST /goals/`

Create a new learning goal.

**Request Body**:
```json
{
  "subject": "Python Programming",
  "topic": "FastAPI Basics",
  "exam_date": "2026-03-15",
  "difficulty": "medium",
  "notes": "Optional notes"
}
```

**Validations**:
- `subject`: 1-200 characters, required
- `topic`: 1-200 characters, required
- `exam_date`: ISO 8601 date format, must be in the future
- `difficulty`: One of "easy", "medium", "hard"
- `notes`: Optional text

**Response**: Created Goal object

#### `GET /goals/{goal_id}`

Get a specific goal by ID.

**Response**: Goal object or 404 error

---

### Content Generation

#### `POST /generate/plan`

Generate a learning plan for a goal.

**Request Body**:
```json
{
  "goal_id": 1,
  "start_date": "2026-01-24"
}
```

**Response**: Array of PlanBlock objects

#### `POST /generate/content`

Generate learning content (flashcards, questions) for a goal.

**Query Parameters**:
- `goal_id`: Integer, required

**Response**: Array of ContentUnit objects

**Example**:
```json
[
  {
    "id": 1,
    "goal_id": 1,
    "type": "flashcard",
    "bloom": "remember",
    "prompt": "What is FastAPI?",
    "answer": "FastAPI is a modern web framework for building APIs with Python",
    "created_at": "2026-01-23T10:00:00"
  }
]
```

#### `POST /generate/expand/explain`

Expand a content unit with more detailed explanation.

**Query Parameters**:
- `content_id`: Integer, required

**Response**: Updated ContentUnit object

---

### Reviews

#### `POST /review/`

Create a new review for a content unit.

**Request Body**:
```json
{
  "content_id": 1,
  "ease": 3
}
```

**Validations**:
- `content_id`: Must exist
- `ease`: Integer 1-5 (1=hard, 5=easy)

**Response**: Created Review object

#### `PUT /review/{review_id}`

Update a review with new ease rating.

**Request Body**:
```json
{
  "ease": 4
}
```

**Response**: ReviewFeedback object (includes review, optional expanded content if ease=1)

#### `GET /review/due`

Get list of reviews that are due.

**Query Parameters**:
- `limit`: Integer, default 20

**Response**: Array of Review objects

---

### Dashboard

#### `GET /dashboard/`

Get dashboard statistics and progress.

**Response**:
```json
{
  "goals": 5,
  "due_reviews": 12,
  "completion_rate": 0.65,
  "today_blocks": [
    {
      "date": "2026-01-23",
      "tasks": [
        {
          "description": "Study FastAPI routing",
          "status": "done"
        }
      ]
    }
  ]
}
```

---

## Error Responses

All endpoints return consistent error responses:

### 404 Not Found
```json
{
  "detail": "Goal with id 123 not found"
}
```

### 422 Validation Error
```json
{
  "detail": "Exam date cannot be in the past"
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred"
}
```

---

## Data Models

### Goal

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| subject | string | Subject name (max 200 chars) |
| topic | string | Topic name (max 200 chars) |
| exam_date | date | Target exam date (ISO 8601) |
| difficulty | enum | "easy", "medium", or "hard" |
| notes | string | Optional notes |
| created_at | datetime | Creation timestamp |

### ContentUnit

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| goal_id | integer | Associated goal ID |
| type | enum | "flashcard", "question", or "drill" |
| bloom | enum | Bloom's taxonomy level |
| prompt | string | Question or prompt text |
| answer | string | Answer or explanation |
| created_at | datetime | Creation timestamp |

**Bloom's Taxonomy Levels**: "remember", "understand", "apply", "analyze", "evaluate", "create"

### Review

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| content_id | integer | Associated content ID |
| ease | integer | Ease rating (1-5) |
| next_due | datetime | Next review date |
| updated_at | datetime | Last update timestamp |

---

## Configuration

The API can be configured via environment variables (create a `.env` file):

```env
# Application
APP_NAME=NeuroLearn API
DEBUG=false

# Database
DATABASE_URL=sqlite:///./neurolearn.db

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# API
API_PREFIX=/api/v1
```

See `.env.example` for a complete configuration template.

---

## Interactive Documentation

When running the server, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
