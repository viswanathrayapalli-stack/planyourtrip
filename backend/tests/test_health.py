from types import SimpleNamespace
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.dependencies import get_current_user, get_db
from app.main import app
from app.shared.metrics.request_metrics import request_metrics


client = TestClient(app)


class FakeDB:
    def execute(self, statement: Any) -> Any:
        if str(statement) != str(text("SELECT 1")):
            raise AssertionError("Unexpected SQL statement")
        return None


def test_live_returns_alive() -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_health_returns_expected_fields() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert "application" in payload
    assert "version" in payload
    assert "environment" in payload
    assert "ai" in payload
    assert "storage" in payload
    assert "timestamp" in payload


def test_live_response_contains_request_id_header() -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


def test_ready_returns_ready_when_database_check_passes() -> None:
    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        response = client.get("/ready")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["checks"]["database"] == "up"
    assert "ai" in payload["checks"]
    assert "storage" in payload["checks"]
    assert "application" in payload
    assert "version" in payload
    assert "environment" in payload
    assert "timestamp" in payload


def test_metrics_requires_authentication() -> None:
    response = client.get("/metrics")

    assert response.status_code == 401
    assert "X-Request-ID" in response.headers


def test_metrics_returns_snapshot_for_authenticated_user() -> None:
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace()

    try:
        response = client.get("/metrics")
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    payload = response.json()
    assert "total_requests" in payload
    assert "requests_by_method" in payload
    assert "requests_by_status" in payload
    assert "requests_by_path" in payload
    assert "total_duration_ms" in payload
    assert "average_duration_ms" in payload


def test_metrics_request_does_not_change_metrics_snapshot() -> None:
    before_snapshot = request_metrics.snapshot()
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace()

    try:
        client.get("/metrics")
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    after_snapshot = request_metrics.snapshot()

    assert after_snapshot == before_snapshot
