# NeuroLearn v0.1

NeuroLearn ist eine minimal funktionsfähige Lernplattform, die Lernziele bündelt,
KI-gestützte Lerninhalte generiert und einen einfachen Spaced-Repetition-Workflow
für Wiederholungen anbietet. Das Projekt besteht aus einem FastAPI-Backend und
einer Next.js-Frontend-Anwendung.

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
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Die API ist anschließend unter <http://localhost:8000> erreichbar. Die
OpenAPI-Dokumentation liegt unter <http://localhost:8000/docs>.

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
