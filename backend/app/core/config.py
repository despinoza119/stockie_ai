"""
Description: Application settings loaded from environment variables via Pydantic BaseSettings.
             Secrets must come from .env or the environment — never hard-coded here.
             All other modules should import `get_settings()` rather than constructing
             Settings themselves, to benefit from caching.
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - File created; added AppSettings with app, server, and logging groups.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Central configuration object for the Stockie AI backend.

    All values are read from environment variables (or a .env file).
    Add new groups here as new infrastructure is introduced (DB, Redis, etc.).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Deployment environment.",
    )
    app_version: str = Field(default="0.1.0", description="Semantic version string.")
    app_debug: bool = Field(default=False, description="Enable debug mode.")

    # ── Server ────────────────────────────────────────────────────────────────
    host: str = Field(default="0.0.0.0", description="Bind address for uvicorn.")
    port: int = Field(default=8000, ge=1, le=65535, description="Bind port for uvicorn.")

    # ── Logging ───────────────────────────────────────────────────────────────
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Minimum log level emitted by the application.",
    )

    @property
    def is_production(self) -> bool:
        """Return True when running in the production environment."""
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return the singleton AppSettings instance (cached after first call).

    Returns:
        The application-wide settings object.
    """
    return AppSettings()
