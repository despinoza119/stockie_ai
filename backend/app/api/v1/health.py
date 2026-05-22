"""
Description: Health-check router.  Exposes GET /health for load-balancer liveness
             probes and the frontend smoke test described in Sprint 0.
             Returns app version, environment, and UTC timestamp.
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - File created; added /health endpoint with HealthResponse model.
"""

from datetime import UTC, datetime

import structlog
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.config import get_settings

router = APIRouter(tags=["health"])
_log = structlog.get_logger(__name__)


class HealthResponse(BaseModel):
    """Shape of the /health response body."""

    status: str = Field(description="Always 'ok' when the service is reachable.")
    version: str = Field(description="Running application version.")
    environment: str = Field(description="Deployment environment (development/staging/production).")
    timestamp: datetime = Field(description="UTC time this response was generated.")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 OK with service metadata.  Used by load balancers and the frontend smoke test.",
)
async def health_check() -> HealthResponse:
    """Return liveness status for the service.

    Returns:
        HealthResponse with status, version, environment, and current UTC timestamp.
    """
    settings = get_settings()
    _log.debug("health check requested")
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        environment=settings.app_env,
        timestamp=datetime.now(UTC),
    )
