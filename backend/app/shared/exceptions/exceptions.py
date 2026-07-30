class AppException(Exception):
    """Base application exception."""

    status_code: int = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class ResourceNotFoundException(AppException):
    """Raised when a resource is not found."""
    status_code = 404

class ResourceAlreadyExistsException(AppException):
    """Raised when attempting to create a resource that already exists."""
    status_code = 409

class ValidationException(AppException):
    """Raised for business validation failures."""
    status_code = 422

class AuthenticationException(AppException):
    """Raised when authentication fails."""
    status_code = 401

class AuthorizationException(AppException):
    """Raised when the user is not authorized."""
    status_code = 403