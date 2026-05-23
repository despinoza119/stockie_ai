"""
Description: Async SQLAlchemy engine and session factory.
             Import `AsyncSessionLocal` to get a database session in FastAPI
             dependencies or Celery tasks.  Import `engine` for Alembic's
             env.py or direct DDL operations.
             Never hard-code connection strings here — they come from AppSettings.
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - File created; async engine, session factory, and get_db dependency.
    2026-05-23 - Added AsyncEngine return type to _build_engine for mypy compliance.
"""

from collections.abc import AsyncIterator

import structlog
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

_log = structlog.get_logger(__name__)


def _build_engine() -> AsyncEngine:
    """Create the async SQLAlchemy engine from current settings.

    Returns:
        AsyncEngine configured from DATABASE_URL in AppSettings.

    Raises:
        ValueError: If DATABASE_URL is not set in the environment.
    """
    settings = get_settings()
    if not settings.database_url:
        raise ValueError("DATABASE_URL is not configured. Set it in your .env file.")
    return create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        echo=settings.app_debug,
    )


engine = _build_engine()

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that yields a database session per request.

    Yields:
        An AsyncSession bound to the current request; commits on success,
        rolls back on any exception.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
