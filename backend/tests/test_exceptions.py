from fastapi.testclient import TestClient

from app.main import app
from app.shared.exceptions.exceptions import AuthenticationException


client = TestClient(app)


def test_authentication_exception_handler_returns_expected_response() -> None:
    @app.get("/test-auth-exception")
    async def test_auth_exception_route() -> None:
        raise AuthenticationException("invalid credentials")

    route = next(route for route in app.router.routes if getattr(route, "path", None) == "/test-auth-exception")

    try:
        response = client.get("/test-auth-exception")
    finally:
        app.router.routes.remove(route)

    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["data"] is None
    assert payload["message"] == "invalid credentials"
    assert payload["request_id"]
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_generic_exception_handler_returns_safe_response() -> None:
    @app.get("/test-generic-exception")
    async def test_generic_exception_route() -> None:
        raise RuntimeError("internal failure details")

    route = next(route for route in app.router.routes if getattr(route, "path", None) == "/test-generic-exception")
    local_client = TestClient(app, raise_server_exceptions=False)

    try:
        response = local_client.get("/test-generic-exception")
    finally:
        app.router.routes.remove(route)
        local_client.close()

    assert response.status_code == 500
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "Internal server error."
    assert payload["data"] is None
    assert payload["request_id"]
    assert "internal failure details" not in response.text
