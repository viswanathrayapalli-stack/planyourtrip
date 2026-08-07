from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_notification_service
from app.modules.notification.schemas import (
    NotificationCreate,
    NotificationResponse,
)
from app.modules.notification.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "/users/{user_id}",
    response_model=list[NotificationResponse],
)
def get_notifications(
    user_id: int,
    db: Session = Depends(get_db),
    service: NotificationService = Depends(get_notification_service),
):
    return service.get_by_user_id(db, user_id)


@router.post(
    "/",
    response_model=NotificationResponse,
)
def create_notification(
    request: NotificationCreate,
    db: Session = Depends(get_db),
    service: NotificationService = Depends(get_notification_service),
):
    return service.create(db, request)


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    service: NotificationService = Depends(get_notification_service),
):
    return service.mark_as_read(db, notification_id)


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    service: NotificationService = Depends(get_notification_service),
):
    service.delete(db, notification_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
