from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.notification.models import Notification
from app.shared.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository[Notification]):

    def __init__(self):
        super().__init__(Notification)

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        return list(db.scalars(stmt).all())


notification_repository = NotificationRepository()
