from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.shared.database.session import get_db
from app.shared.schemas import MessageResponse

from app.core.dependencies import get_user_service

from app.modules.user.schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.modules.user.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.get_all(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.get_by_id(db, user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: UserCreate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.create(db, request)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.update(
        db=db,
        user_id=user_id,
        request=request,
    )


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    service.delete(db, user_id)

    return MessageResponse(
        success=True,
        message="User deleted successfully.",
    )