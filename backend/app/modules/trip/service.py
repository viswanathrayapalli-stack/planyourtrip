from sqlalchemy.orm import Session

from app.modules.trip.models import Trip
from app.modules.trip.repository import TripRepository
from app.modules.trip.schemas import TripCreate, TripResponse, TripUpdate
from app.shared.authorization import AuthorizationService
from app.shared.pagination import PageResponse, PaginationParams


class TripService:

    def __init__(
        self,
        repository: TripRepository,
        authorization_service: AuthorizationService,
    ):
        self.repository = repository
        self.authorization_service = authorization_service

    def get_all(
        self,
        db: Session,
        user_id: int,
    ) -> list[Trip]:
        return self.repository.get_all_by_user(db, user_id)

    def get_all_paginated(
        self,
        db: Session,
        user_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[TripResponse]:
        page = self.repository.get_all_by_user_paginated(
            db=db,
            user_id=user_id,
            pagination=pagination,
        )

        return PageResponse(
            items=[TripResponse.model_validate(trip) for trip in page.items],
            total=page.total,
            page=page.page,
            page_size=page.page_size,
            total_pages=page.total_pages,
        )

    def get_by_id(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> Trip:
        return self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

    def create(
        self,
        db: Session,
        user_id: int,
        request: TripCreate,
    ) -> Trip:

        trip = Trip(**request.model_dump(), user_id=user_id)

        return self.repository.create(db, trip)

    def update(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
        request: TripUpdate,
    ) -> Trip:

        trip = self.get_by_id(db, trip_id, user_id)

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(trip, key, value)

        return self.repository.update(db, trip)

    def delete(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> None:

        trip = self.get_by_id(db, trip_id, user_id)

        self.repository.delete(db, trip)