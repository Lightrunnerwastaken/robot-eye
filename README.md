# NeuroLearn v0.1

NeuroLearn ist eine minimal funktionsfähige Lernplattform, die Lernziele bündelt,
KI-gestützte Lerninhalte generiert und einen einfachen Spaced-Repetition-Workflow
für Wiederholungen anbietet. Das Projekt besteht aus einem FastAPI-Backend und
einer Next.js-Frontend-Anwendung.

## 🚀 Recent Improvements (v0.1.1)

This version includes significant improvements to code quality, security, and maintainability:

### ✅ Security & Configuration
- **Environment-based configuration** with `.env` support
- **Secure CORS policy** (no longer allows all origins)
- **Input validation** with Pydantic v2 enums and validators
- **Comprehensive error handling** with custom exception handlers

### ✅ Code Quality
- **Structured logging** throughout the application
- **Centralized dependencies** (no more duplicated code)
- **Database indexing** for improved query performance
- **Type safety** with proper enum validation
- **Pydantic v2 migration** for better performance

### ✅ Testing & Documentation
- **Pytest configuration** with test fixtures
- **Unit tests** for critical endpoints
- **Comprehensive API documentation** (see `backend/API.md`)
- **Development requirements** for testing tools

## Projektüberblick

- **Backend** – FastAPI + SQLAlchemy + SQLite für Lernziele, Inhalte, Pläne und
  Wiederholungen. Enthält Mock-Generatoren für Lernpläne und Lernmaterialien.
- **Frontend** – Next.js (TypeScript) + Tailwind CSS + React Query zur Erfassung
  von Lernzielen, Anzeige des Dashboards und Bearbeitung von Wiederholungen.
- **Infra** – Platz für Deployment-Artefakte oder Infrastruktur-Skripte.

## Schnellstart

### Voraussetzungen

- Python 3.11+
- Node.js 18+
- npm oder yarn

### Backend starten

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install development dependencies (for testing)
pip install -r requirements-dev.txt

# Optional: Configure environment variables
cp .env.example .env
# Edit .env with your settings

# Start the server
uvicorn backend.main:app --reload
```

Die API ist anschließend unter <http://localhost:8000> erreichbar. Die
OpenAPI-Dokumentation liegt unter <http://localhost:8000/docs>.

**API Documentation**: See `backend/API.md` for detailed endpoint documentation.

### Frontend starten

```bash
cd frontend
npm install
npm run dev
```

Das Frontend läuft unter <http://localhost:3000> und erwartet das Backend unter
`http://localhost:8000`.

## Projektstruktur

```
.
├── backend
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── prompts/
├── frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── styles/
│   └── tailwind.config.ts
├── infra
│   └── README.md
└── README.md
```

## Entwicklungshinweise

1. **Migrationsstrategie** – Für das MVP wird die Datenbank automatisch über
   SQLAlchemy-Modelle initialisiert. Für spätere Releases empfiehlt sich Alembic.
2. **LLM-Anbindung** – Der Mock in `backend/services/llm_provider.py` soll durch
   eine echte LLM-Integration ersetzt werden (z. B. OpenAI, Azure, lokale Modelle).
3. **Tests & CI** – Unit-Tests und Pipeline-Konfiguration sind vorgesehen für
   Meilenstein M5.

## Demo-Daten

Zum schnellen Einstieg bietet `backend/seed.py` ein Skript, das Muster-Lernziele
und Lerninhalte erzeugt:

```bash
cd backend
python seed.py
```

## Lizenz

Dieses Repository dient als Ausgangspunkt für das NeuroLearn-Projekt und steht
unter MIT-Lizenz. Weitere Lizenzinformationen für abhängige Bibliotheken siehe
die jeweiligen Projekte.

## Testing

Run unit tests with pytest:

```bash
cd backend
pip install -r requirements-dev.txt
pytest

# With coverage report
pytest --cov=backend --cov-report=html
```

## Configuration

Create a `.env` file based on `.env.example`:

```bash
cd backend
cp .env.example .env
# Edit .env with your settings
```

**Available Environment Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | NeuroLearn API |
| `DEBUG` | Debug mode | false |
| `DATABASE_URL` | Database connection | sqlite:///./neurolearn.db |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | http://localhost:3000 |
| `API_PREFIX` | API route prefix | (empty) |

## Code Quality Features

- ✅ **Structured Logging** - All operations are logged for debugging
- ✅ **Input Validation** - Pydantic v2 with custom validators
- ✅ **Error Handling** - Custom exception handlers
- ✅ **Database Indexing** - Optimized queries with proper indexes
- ✅ **Type Safety** - Full type hints throughout
- ✅ **Security** - Configurable CORS, input sanitization
