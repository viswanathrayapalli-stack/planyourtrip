from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user
from app.main import app
from app.shared.metrics.request_metrics import request_metrics


client = TestClient(app)


def test_successful_request_is_recorded_in_metrics() -> None:
    before = request_metrics.snapshot()

    response = client.get("/live")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers

    after = request_metrics.snapshot()

    assert after["total_requests"] == before["total_requests"] + 1
    assert after["requests_by_method"]["GET"] == before["requests_by_method"].get("GET", 0) + 1
    assert after["requests_by_path"]["/live"] == before["requests_by_path"].get("/live", 0) + 1
    assert after["requests_by_status"]["200"] == before["requests_by_status"].get("200", 0) + 1
    assert after["total_duration_ms"] >= before["total_duration_ms"]
    assert after["average_duration_ms"] >= 0.0


def test_failed_request_is_not_silently_recorded_as_success() -> None:
    @app.get("/test-failed-request")
    async def test_failed_request_route() -> None:
        raise RuntimeError("boom")

    route = next(route for route in app.router.routes if getattr(route, "path", None) == "/test-failed-request")
    local_client = TestClient(app, raise_server_exceptions=False)

    before = request_metrics.snapshot()

    try:
        response = local_client.get("/test-failed-request")
    finally:
        app.router.routes.remove(route)
        local_client.close()

    assert response.status_code == 500

    after = request_metrics.snapshot()

    assert after["total_requests"] == before["total_requests"] + 1
    assert after["requests_by_path"]["/test-failed-request"] == before["requests_by_path"].get("/test-failed-request", 0) + 1
    assert after["requests_by_status"]["ERROR"] == before["requests_by_status"].get("ERROR", 0) + 1


def test_metrics_endpoint_does_not_change_request_metrics() -> None:
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace()

    before = request_metrics.snapshot()

    try:
        response = client.get("/metrics")
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200

    after = request_metrics.snapshot()
    assert after == before
