"""
Description: Tests for the /health endpoint.
             Verifies response shape, HTTP status, and field invariants.
Last Modified By: bvela
Created: 2026-05-22
Last Modified:
    2026-05-22 - File created; added happy-path and field-shape tests.
    2026-05-23 - Removed local client fixture; now provided by tests/conftest.py.
"""

from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_status_is_ok(client: TestClient) -> None:
    data = client.get("/health").json()
    assert data["status"] == "ok"


def test_health_version_present(client: TestClient) -> None:
    data = client.get("/health").json()
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


def test_health_environment_present(client: TestClient) -> None:
    data = client.get("/health").json()
    assert data["environment"] in {"development", "staging", "production"}


def test_health_timestamp_is_iso(client: TestClient) -> None:
    from datetime import datetime

    data = client.get("/health").json()
    datetime.fromisoformat(data["timestamp"])
