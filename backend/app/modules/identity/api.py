from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.modules.identity.constants import LOGIN_SUCCESS
from app.modules.identity.schemas import (
    CurrentUserResponse,
    LoginRequest,
    TokenResponse,
)
from app.modules.identity.service import identity_service
from app.modules.user.models import User
from app.shared.database.session import get_db
from app.shared.schemas.api_response import ApiResponse
from app.shared.utils.response import success_response
from app.modules.identity.constants import (
    CURRENT_USER_RETRIEVED,
    LOGIN_SUCCESS,
)

router = APIRouter(
    prefix="/identity",
    tags=["Identity"],
)


@router.post(
    "/login",
    response_model=ApiResponse[TokenResponse],
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    token = identity_service.login(
        db=db,
        request=request,
    )

    return success_response(
        data=token,
        message=LOGIN_SUCCESS,
    )


@router.get(
    "/me",
    response_model=ApiResponse[CurrentUserResponse],
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return success_response(
        data=CurrentUserResponse.model_validate(current_user),
        message="Current user retrieved successfully.",
    )
    return success_response(
    data=CurrentUserResponse.model_validate(current_user),
    message=CURRENT_USER_RETRIEVED,
)