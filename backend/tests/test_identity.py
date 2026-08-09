from fastapi.testclient import TestClient

from app.core.dependencies import get_db
from app.core.security import hash_password
from app.main import app


client = TestClient(app)


def test_login_success_returns_token_response() -> None:
    class FakeUser:
        id = 1
        is_active = True
        password_hash = hash_password("password")

    class FakeLoginDB:
        def scalar(self, statement: object) -> object:
            return FakeUser()

    def fake_get_db() -> FakeLoginDB:
        return FakeLoginDB()

    app.dependency_overrides[get_db] = fake_get_db

    try:
        response = client.post(
            "/api/v1/identity/login",
            data={"username": "user@example.com", "password": "password"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    payload = response.json()
    assert "access_token" in payload
    assert payload["token_type"] == "bearer"
    assert payload["expires_in"] > 0


def test_login_with_invalid_credentials_returns_authentication_error() -> None:
    class FakeLoginDB:
        def scalar(self, statement: object) -> object:
            return None

    def fake_get_db() -> FakeLoginDB:
        return FakeLoginDB()

    app.dependency_overrides[get_db] = fake_get_db

    try:
        response = client.post(
            "/api/v1/identity/login",
            data={"username": "user@example.com", "password": "wrong-password"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["data"] is None
    assert payload["message"] == "Invalid email or password."
    assert payload["request_id"]
