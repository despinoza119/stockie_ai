"""
Description: Structured logging configuration using structlog.
             In development: colorful, human-readable console output.
             In production: newline-delimited JSON suitable for log aggregators.
             Call configure_logging() once at application startup (in main.py).
             All other modules obtain a logger via structlog.get_logger(__name__).
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - File created; development (pretty) and production (JSON) renderers.
"""

import logging
import sys
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from app.core.config import AppSettings


def configure_logging(settings: "AppSettings") -> None:
    """Configure structlog and the stdlib logging root handler.

    Must be called once before the first log statement.  Subsequent calls are
    safe (structlog is idempotent when called with the same configuration) but
    unnecessary.

    Args:
        settings: Application settings used to determine log level and renderer.
    """
    log_level = getattr(logging, settings.log_level, logging.INFO)

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.is_production:
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Silence noisy third-party loggers in non-debug environments.
    if not settings.app_debug:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
