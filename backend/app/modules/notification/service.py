from sqlalchemy.orm import Session

from app.modules.notification.repository import NotificationRepository
from app.modules.notification.schemas import NotificationCreate, NotificationResponse
from app.modules.user.repository import UserRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException


class NotificationService:

    def __init__(
        self,
        repository: NotificationRepository,
        user_repository: UserRepository,
    ):
        self.repository = repository
        self.user_repository = user_repository

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> list[NotificationResponse]:
        user = self.user_repository.get_by_id(db, user_id)

        if user is None:
            raise ResourceNotFoundException("User not found.")

        notifications = self.repository.get_by_user_id(db, user_id)

        response: list[NotificationResponse] = []

        for n in notifications:
            response.append(
                NotificationResponse(
                    id=n.id,
                    user_id=n.user_id,
                    title=n.title,
                    message=n.message,
                    notification_type=n.notification_type,
                    is_read=n.is_read,
                    created_at=n.created_at,
                )
            )

        return response

    def create(
        self,
        db: Session,
        request: NotificationCreate,
    ) -> NotificationResponse:
        user = self.user_repository.get_by_id(db, request.user_id)

        if user is None:
            raise ResourceNotFoundException("User not found.")

        notification = self.repository.model(**request.model_dump())
        notification = self.repository.create(db, notification)

        return NotificationResponse(
            id=notification.id,
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            notification_type=notification.notification_type,
            is_read=notification.is_read,
            created_at=notification.created_at,
        )

    def mark_as_read(
        self,
        db: Session,
        notification_id: int,
    ) -> NotificationResponse:
        notification = self.repository.get_by_id(db, notification_id)

        if notification is None:
            raise ResourceNotFoundException("Notification not found.")

        notification.is_read = True
        notification = self.repository.update(db, notification)

        return NotificationResponse(
            id=notification.id,
            user_id=notification.user_id,
            title=notification.title,
            message=notification.message,
            notification_type=notification.notification_type,
            is_read=notification.is_read,
            created_at=notification.created_at,
        )

    def delete(
        self,
        db: Session,
        notification_id: int,
    ) -> None:
        notification = self.repository.get_by_id(db, notification_id)

        if notification is None:
            raise ResourceNotFoundException("Notification not found.")

        self.repository.delete(db, notification)
