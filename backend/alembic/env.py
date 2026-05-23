"""
Description: Alembic migration environment.  Configures the async SQLAlchemy
             engine from AppSettings and wires Base.metadata so that
             `alembic revision --autogenerate` detects schema changes.
             Run migrations:     uv run alembic upgrade head
             Generate revision:  uv run alembic revision --autogenerate -m "<msg>"
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - File created; async online/offline modes, autogenerate support.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine

import app.models  # noqa: F401  — registers concrete models on Base.metadata
from alembic import context
from app.core.config import get_settings

# Import Base and all model modules so autogenerate sees the full schema.
# Add new model imports here as they are created in later sprints.
from app.models.base import Base  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _get_url() -> str:
    url = get_settings().database_url
    if not url:
        raise ValueError("DATABASE_URL is not set. Cannot run migrations.")
    return url


# ── Offline mode — emits SQL script, no live connection needed ────────────────


def run_migrations_offline() -> None:
    """Emit migration SQL to stdout without a live DB connection."""
    context.configure(
        url=_get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online mode — runs against a live async DB connection ─────────────────────


def _do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Connect to the DB and apply pending migrations."""
    connectable = create_async_engine(_get_url())
    async with connectable.connect() as connection:
        await connection.run_sync(_do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
