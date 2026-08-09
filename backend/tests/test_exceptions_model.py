from app.shared.exceptions.exceptions import (
    AppException,
    AuthenticationException,
    AuthorizationException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
    ValidationException,
)


def test_app_exception_preserves_message_and_status_code() -> None:
    exception = AppException("test error")

    assert exception.message == "test error"
    assert str(exception) == "test error"
    assert exception.status_code == 400
    assert isinstance(exception, Exception)


def test_resource_not_found_exception_uses_expected_status_code() -> None:
    exception = ResourceNotFoundException("resource not found")

    assert exception.message == "resource not found"
    assert exception.status_code == 404
    assert isinstance(exception, AppException)


def test_resource_already_exists_exception_uses_expected_status_code() -> None:
    exception = ResourceAlreadyExistsException("resource already exists")

    assert exception.message == "resource already exists"
    assert exception.status_code == 409
    assert isinstance(exception, AppException)


def test_validation_exception_uses_expected_status_code() -> None:
    exception = ValidationException("validation failed")

    assert exception.message == "validation failed"
    assert exception.status_code == 422
    assert isinstance(exception, AppException)


def test_authentication_exception_uses_expected_status_code() -> None:
    exception = AuthenticationException("authentication failed")

    assert exception.message == "authentication failed"
    assert exception.status_code == 401
    assert isinstance(exception, AppException)


def test_authorization_exception_uses_expected_status_code() -> None:
    exception = AuthorizationException("authorization failed")

    assert exception.message == "authorization failed"
    assert exception.status_code == 403
    assert isinstance(exception, AppException)
