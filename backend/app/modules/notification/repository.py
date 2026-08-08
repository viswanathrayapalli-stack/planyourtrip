from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.notification.models import Notification
from app.shared.query_builder import QueryBuilder
from app.shared.pagination import PageResponse, PaginationParams
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

    def get_by_user_id_paginated(
        self,
        db: Session,
        user_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[Notification]:
        builder = QueryBuilder(
            select(Notification).where(Notification.user_id == user_id)
        )
        builder.order_by(Notification.created_at.desc())

        stmt = builder.build()
        return self.paginate(
            db=db,
            stmt=stmt,
            pagination=pagination,
        )


notification_repository = NotificationRepository()
