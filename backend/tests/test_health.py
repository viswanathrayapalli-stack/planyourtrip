from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.dependencies import get_db
from app.main import app


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


def test_request_id_is_unique_across_requests() -> None:
    first_response = client.get("/live")
    second_response = client.get("/live")

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_request_id = first_response.headers.get("X-Request-ID")
    second_request_id = second_response.headers.get("X-Request-ID")

    assert first_request_id
    assert second_request_id
    assert isinstance(first_request_id, str)
    assert isinstance(second_request_id, str)
    assert first_request_id != second_request_id


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


def test_ready_returns_not_ready_when_database_check_fails() -> None:
    class FailingDB:
        def execute(self, statement: Any) -> Any:
            raise SQLAlchemyError("database down")

    app.dependency_overrides[get_db] = lambda: FailingDB()

    try:
        response = client.get("/ready")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "not_ready"
    assert payload["checks"]["database"] == "down"
    assert "ai" in payload["checks"]
    assert "storage" in payload["checks"]
    assert "application" in payload
    assert "version" in payload
    assert "environment" in payload
    assert "timestamp" in payload
