from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.main import app
from app.shared.metrics.request_metrics import request_metrics


client = TestClient(app)


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
