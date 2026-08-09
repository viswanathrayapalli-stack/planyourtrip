from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core import dependencies as core_dependencies
from app.core.dependencies import get_db
from app.core.security import create_access_token, hash_password
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


def test_current_user_profile_requires_authentication() -> None:
    response = client.get("/api/v1/identity/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_current_user_profile_rejects_invalid_token() -> None:
    response = client.get(
        "/api/v1/identity/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["data"] is None
    assert payload["request_id"]


def test_current_user_profile_rejects_token_without_subject() -> None:
    class FakeDB:
        pass

    token = create_access_token({"role": "user"})

    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        response = client.get(
            "/api/v1/identity/me",
            headers={"Authorization": f"Bearer {token}"},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["data"] is None
    assert payload["request_id"]


def test_current_user_profile_rejects_nonexistent_user() -> None:
    class FakeDB:
        pass

    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        with patch.object(core_dependencies.user_repository, "get_by_id", return_value=None):
            token = create_access_token({"sub": "999999"})
            response = client.get(
                "/api/v1/identity/me",
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["data"] is None
    assert payload["request_id"]


def test_current_user_profile_rejects_inactive_user() -> None:
    class FakeDB:
        pass

    fake_user = SimpleNamespace(
        id=8,
        is_active=False,
    )

    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        with patch.object(core_dependencies.user_repository, "get_by_id", return_value=fake_user):
            token = create_access_token({"sub": str(fake_user.id)})
            response = client.get(
                "/api/v1/identity/me",
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 401
    payload = response.json()
    assert payload["success"] is False
    assert payload["data"] is None
    assert payload["request_id"]


def test_current_user_profile_returns_current_user() -> None:
    class FakeDB:
        pass

    fake_user = SimpleNamespace(
        id=7,
        full_name="Test User",
        email="user@example.com",
        is_active=True,
    )

    app.dependency_overrides[get_db] = lambda: FakeDB()

    try:
        with patch.object(core_dependencies.user_repository, "get_by_id", return_value=fake_user):
            token = create_access_token({"sub": str(fake_user.id)})
            response = client.get(
                "/api/v1/identity/me",
                headers={"Authorization": f"Bearer {token}"},
            )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"] is not None
    assert payload["data"]["id"] == fake_user.id
    assert payload["data"]["full_name"] == fake_user.full_name
    assert payload["data"]["email"] == fake_user.email
    assert payload["data"]["is_active"] is True
