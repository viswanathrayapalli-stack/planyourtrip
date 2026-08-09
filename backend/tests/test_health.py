from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


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
