from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import Base, engine
from backend.exceptions import (
    DatabaseError,
    ValidationError,
    database_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)
from backend.logging_config import logger
from backend.routes import dashboard, generate, goals, review

# Initialize database
Base.metadata.create_all(bind=engine)
logger.info("Database initialized")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS configured for origins: {settings.cors_origins}")

# Register exception handlers
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(DatabaseError, database_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(goals.router, prefix=settings.api_prefix)
app.include_router(generate.router, prefix=settings.api_prefix)
app.include_router(review.router, prefix=settings.api_prefix)
app.include_router(dashboard.router, prefix=settings.api_prefix)


@app.get("/health")
def healthcheck():
    """Health check endpoint."""
    logger.debug("Health check requested")
    return {"status": "ok", "version": settings.app_version}
