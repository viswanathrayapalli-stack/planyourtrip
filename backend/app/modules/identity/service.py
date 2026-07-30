from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.core.settings import settings
from app.modules.identity.constants import (
    INACTIVE_USER,
    INVALID_CREDENTIALS,
)
from app.modules.identity.schemas import (
    LoginRequest,
    TokenResponse,
)
from app.modules.user.repository import user_repository
from app.shared.exceptions.exceptions import AuthenticationException


class IdentityService:
    """Business logic for authentication."""

    def login(
        self,
        db: Session,
        request: LoginRequest,
    ) -> TokenResponse:

        user = user_repository.get_by_email(
            db=db,
            email=request.email,
        )

        if user is None:
            raise AuthenticationException(INVALID_CREDENTIALS)

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise AuthenticationException(INVALID_CREDENTIALS)

        if not user.is_active:
            raise AuthenticationException(INACTIVE_USER)

        token = create_access_token(
            {
                "sub": str(user.id),
            }
        )

        return TokenResponse(
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
        )


identity_service = IdentityService()