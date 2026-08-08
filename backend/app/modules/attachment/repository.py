from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.attachment.models import Attachment
from app.shared.query_builder import QueryBuilder
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.repositories.base_repository import BaseRepository


class AttachmentRepository(BaseRepository[Attachment]):

    def __init__(self):
        super().__init__(Attachment)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Attachment]:
        stmt = (
            select(Attachment)
            .where(Attachment.trip_id == trip_id)
            .order_by(Attachment.created_at.desc())
        )
        return list(db.scalars(stmt).all())

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[Attachment]:
        builder = QueryBuilder(
            select(Attachment).where(Attachment.trip_id == trip_id)
        )
        builder.order_by(Attachment.created_at.desc())

        stmt = builder.build()
        return self.paginate(
            db=db,
            stmt=stmt,
            pagination=pagination,
        )


attachment_repository = AttachmentRepository()
