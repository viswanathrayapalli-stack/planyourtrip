from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.note.models import Note
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.repositories.base_repository import BaseRepository


class NoteRepository(BaseRepository[Note]):

    def __init__(self):
        super().__init__(Note)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.trip_id == trip_id)
            .order_by(Note.created_at.desc())
        )

        return list(db.scalars(stmt).all())

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[Note]:
        stmt = (
            select(Note)
            .where(Note.trip_id == trip_id)
            .order_by(Note.created_at.desc())
        )
        return self.paginate(
            db=db,
            stmt=stmt,
            pagination=pagination,
        )


note_repository = NoteRepository()
