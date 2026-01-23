"""Logging configuration for NeuroLearn backend."""
from __future__ import annotations

import logging
import sys
from typing import Any

from backend.config import settings


def setup_logging() -> logging.Logger:
    """Configure application logging."""
    log_level = logging.DEBUG if settings.debug else logging.INFO

    # Create logger
    logger = logging.getLogger("neurolearn")
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers = []

    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logging()


def log_request(method: str, path: str, **kwargs: Any) -> None:
    """Log HTTP request details."""
    logger.info(f"{method} {path}", extra=kwargs)


def log_error(message: str, exc: Exception | None = None, **kwargs: Any) -> None:
    """Log error with optional exception."""
    if exc:
        logger.error(f"{message}: {exc}", exc_info=True, extra=kwargs)
    else:
        logger.error(message, extra=kwargs)
