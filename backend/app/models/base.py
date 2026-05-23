"""
Description: Declarative base for all SQLAlchemy ORM models.
             Every model must inherit from Base so that Alembic autogenerate
             can discover the full schema through Base.metadata.
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - File created.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
