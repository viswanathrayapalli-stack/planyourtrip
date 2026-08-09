from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from pydantic import ValidationError

from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate, UserResponse, UserUpdate
from app.modules.user.service import UserService
from app.shared.exceptions.exceptions import (
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)


def test_user_repository_get_by_email_returns_user_when_scalar_returns_user() -> None:
    db = Mock()
    expected_user = SimpleNamespace(id=1)
    db.scalar.return_value = expected_user

    repository = UserRepository()
    result = repository.get_by_email(db, "user@example.com")

    assert result is expected_user
    db.scalar.assert_called_once()

    statement = db.scalar.call_args.args[0]
    assert statement is not None

    compiled = statement.compile(compile_kwargs={"literal_binds": True})
    assert "users" in str(compiled)
    assert "user@example.com" in str(compiled)


def test_user_repository_get_by_email_returns_none_when_scalar_returns_none() -> None:
    db = Mock()
    db.scalar.return_value = None

    repository = UserRepository()
    result = repository.get_by_email(db, "user@example.com")

    assert result is None
    db.scalar.assert_called_once()

    statement = db.scalar.call_args.args[0]
    assert statement is not None

    compiled = statement.compile(compile_kwargs={"literal_binds": True})
    assert "users" in str(compiled)
    assert "user@example.com" in str(compiled)


def test_user_service_get_all_returns_repository_result_unchanged() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    expected_users = [SimpleNamespace(id=1)]
    repository.get_all.return_value = expected_users

    result = service.get_all(db)

    assert result is expected_users
    repository.get_all.assert_called_once_with(db)


def test_user_service_get_by_id_returns_existing_user() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    expected_user = SimpleNamespace(id=1)
    repository.get_by_id.return_value = expected_user

    result = service.get_by_id(db, 1)

    assert result is expected_user
    repository.get_by_id.assert_called_once_with(db, 1)


def test_user_service_get_by_id_raises_when_user_missing() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException) as exc_info:
        service.get_by_id(db, 1)

    assert str(exc_info.value) == "User not found."
    assert exc_info.value.message == "User not found."
    repository.get_by_id.assert_called_once_with(db, 1)


def test_user_service_create_returns_created_user_and_hashes_password() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    request = UserCreate(
        full_name="Jane Doe",
        email="jane@example.com",
        password="secret1234",
    )
    created_user = SimpleNamespace(id=1)
    repository.get_by_email.return_value = None
    repository.create.return_value = created_user

    with patch("app.modules.user.service.hash_password", return_value="hashed-password") as hash_mock:
        result = service.create(db, request)

    assert result is created_user
    hash_mock.assert_called_once_with("secret1234")
    repository.get_by_email.assert_called_once_with(db, request.email)

    created_user_arg = repository.create.call_args.args[1]
    assert isinstance(created_user_arg, User)
    assert created_user_arg.full_name == request.full_name
    assert created_user_arg.email == request.email
    assert created_user_arg.password_hash == "hashed-password"
    assert created_user_arg.is_active is True


def test_user_service_create_raises_for_duplicate_email_without_hashing_or_creating() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    request = UserCreate(
        full_name="Jane Doe",
        email="jane@example.com",
        password="secret1234",
    )
    repository.get_by_email.return_value = SimpleNamespace(id=99)

    with patch("app.modules.user.service.hash_password") as hash_mock:
        with pytest.raises(ResourceAlreadyExistsException) as exc_info:
            service.create(db, request)

    assert str(exc_info.value) == "Email is already registered."
    assert exc_info.value.message == "Email is already registered."
    hash_mock.assert_not_called()
    repository.create.assert_not_called()


def test_user_service_update_updates_fields_without_password() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    existing_user = SimpleNamespace(
        id=1,
        full_name="Old Name",
        password_hash="old-hash",
        is_active=True,
    )
    repository.get_by_id.return_value = existing_user
    updated_user = SimpleNamespace(id=1)
    repository.update.return_value = updated_user
    request = UserUpdate(full_name="New Name", is_active=False)

    result = service.update(db, 1, request)

    assert result is updated_user
    assert existing_user.full_name == "New Name"
    assert existing_user.is_active is False
    assert existing_user.password_hash == "old-hash"
    repository.update.assert_called_once_with(db, existing_user)


def test_user_service_update_hashes_new_password_and_avoids_plain_password_assignment() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    existing_user = SimpleNamespace(
        id=1,
        full_name="Old Name",
        password_hash="old-hash",
        is_active=True,
    )
    repository.get_by_id.return_value = existing_user
    updated_user = SimpleNamespace(id=1)
    repository.update.return_value = updated_user
    request = UserUpdate(password="new-password")

    with patch("app.modules.user.service.hash_password", return_value="new-hash") as hash_mock:
        result = service.update(db, 1, request)

    assert result is updated_user
    hash_mock.assert_called_once_with("new-password")
    assert existing_user.password_hash == "new-hash"
    assert not hasattr(existing_user, "password")
    repository.update.assert_called_once_with(db, existing_user)


def test_user_service_update_raises_when_user_missing() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException) as exc_info:
        service.update(db, 1, UserUpdate(full_name="New Name"))

    assert str(exc_info.value) == "User not found."
    repository.update.assert_not_called()


def test_user_service_delete_returns_none_for_existing_user() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    existing_user = SimpleNamespace(id=1)
    repository.get_by_id.return_value = existing_user

    result = service.delete(db, 1)

    assert result is None
    repository.delete.assert_called_once_with(db, existing_user)


def test_user_service_delete_raises_for_missing_user_without_deleting() -> None:
    repository = Mock()
    service = UserService(repository)
    db = object()
    repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException) as exc_info:
        service.delete(db, 1)

    assert str(exc_info.value) == "User not found."
    repository.delete.assert_not_called()


def test_user_create_schema_accepts_valid_values() -> None:
    request = UserCreate(
        full_name="Jane Doe",
        email="jane@example.com",
        password="secret1234",
    )

    assert request.full_name == "Jane Doe"
    assert request.email == "jane@example.com"
    assert request.password == "secret1234"


@pytest.mark.parametrize(
    ("full_name", "email", "password"),
    [
        ("J", "jane@example.com", "secret1234"),
        ("x" * 101, "jane@example.com", "secret1234"),
        ("Jane Doe", "not-an-email", "secret1234"),
        ("Jane Doe", "jane@example.com", "short"),
        ("Jane Doe", "jane@example.com", "x" * 101),
    ],
)
def test_user_create_schema_rejects_invalid_values(full_name: str, email: str, password: str) -> None:
    with pytest.raises(ValidationError):
        UserCreate(full_name=full_name, email=email, password=password)


def test_user_update_schema_accepts_empty_payload() -> None:
    request = UserUpdate()

    assert request.full_name is None
    assert request.password is None
    assert request.is_active is None


def test_user_update_schema_accepts_valid_values() -> None:
    request = UserUpdate(full_name="Jane Doe", password="secret1234", is_active=False)

    assert request.full_name == "Jane Doe"
    assert request.password == "secret1234"
    assert request.is_active is False


@pytest.mark.parametrize(
    ("full_name", "password"),
    [
        ("J", "secret1234"),
        ("Jane Doe", "short"),
    ],
)
def test_user_update_schema_rejects_invalid_values(full_name: str, password: str) -> None:
    with pytest.raises(ValidationError):
        UserUpdate(full_name=full_name, password=password)


def test_user_response_schema_converts_from_attributes() -> None:
    user = SimpleNamespace(
        id=1,
        full_name="Jane Doe",
        email="jane@example.com",
        is_active=True,
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    )

    response = UserResponse.model_validate(user)

    assert response.id == 1
    assert response.full_name == "Jane Doe"
    assert response.email == "jane@example.com"
    assert response.is_active is True
