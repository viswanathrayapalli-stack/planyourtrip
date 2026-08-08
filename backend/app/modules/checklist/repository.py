from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.checklist.models import Checklist
from app.shared.query_builder import QueryBuilder
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.repositories.base_repository import BaseRepository


class ChecklistRepository(BaseRepository[Checklist]):

    def __init__(self):
        super().__init__(Checklist)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Checklist]:
        stmt = (
            select(Checklist)
            .where(Checklist.trip_id == trip_id)
            .order_by(Checklist.due_date.asc())
        )

        return list(db.scalars(stmt).all())

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[Checklist]:
        builder = QueryBuilder(
            select(Checklist).where(Checklist.trip_id == trip_id)
        )
        builder.order_by(Checklist.created_at.desc())

        stmt = builder.build()
        return self.paginate(
            db=db,
            stmt=stmt,
            pagination=pagination,
        )


checklist_repository = ChecklistRepository()
