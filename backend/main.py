from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routes import dashboard, generate, goals, review

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NeuroLearn API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(goals.router)
app.include_router(generate.router)
app.include_router(review.router)
app.include_router(dashboard.router)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
