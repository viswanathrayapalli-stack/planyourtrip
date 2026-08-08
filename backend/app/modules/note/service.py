from sqlalchemy.orm import Session

from app.modules.note.constants import NOTE_NOT_FOUND
from app.modules.note.models import Note
from app.modules.note.repository import NoteRepository
from app.modules.note.schemas import NoteCreate, NoteResponse, NoteUpdate
from app.shared.authorization import AuthorizationService
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException
from app.shared.pagination import PageResponse, PaginationParams


class NoteService:

    def __init__(
        self,
        repository: NoteRepository,
        trip_repository: TripRepository,
        authorization_service: AuthorizationService,
    ):
        self.repository = repository
        self.trip_repository = trip_repository
        self.authorization_service = authorization_service

    def get_all(
        self,
        db: Session,
    ) -> list[Note]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        note_id: int,
        user_id: int,
    ) -> Note:
        note = self.repository.get_by_id(db, note_id)

        if note is None:
            raise ResourceNotFoundException(NOTE_NOT_FOUND)

        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=note.trip_id,
            current_user_id=user_id,
        )

        return note

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> list[Note]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        return self.repository.get_by_trip_id(db, trip_id)

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[NoteResponse]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        page = self.repository.get_by_trip_id_paginated(
            db=db,
            trip_id=trip_id,
            pagination=pagination,
        )

        return PageResponse(
            items=[
                NoteResponse.model_validate(item)
                for item in page.items
            ],
            total=page.total,
            page=page.page,
            page_size=page.page_size,
            total_pages=page.total_pages,
        )

    def create(
        self,
        db: Session,
        request: NoteCreate,
        user_id: int,
    ) -> Note:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=request.trip_id,
            current_user_id=user_id,
        )

        note = Note(**request.model_dump())

        return self.repository.create(db, note)

    def update(
        self,
        db: Session,
        note_id: int,
        request: NoteUpdate,
        user_id: int,
    ) -> Note:
        note = self.get_by_id(db, note_id, user_id)
        update_data = request.model_dump(exclude_unset=True)


        for key, value in update_data.items():
            setattr(note, key, value)

        return self.repository.update(db, note)

    def delete(
        self,
        db: Session,
        note_id: int,
        user_id: int,
    ) -> None:
        note = self.get_by_id(db, note_id, user_id)
        self.repository.delete(db, note)
