from sqlalchemy.orm import Session

from app.modules.trip.models import Trip
from app.modules.trip.repository import TripRepository
from app.modules.trip.schemas import TripCreate, TripUpdate
from app.shared.exceptions.exceptions import ResourceNotFoundException


class TripService:

    def __init__(
        self,
        repository: TripRepository,
    ):
        self.repository = repository

    def get_all(
        self,
        db: Session,
    ) -> list[Trip]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        trip_id: int,
    ) -> Trip:

        trip = self.repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        return trip

    def create(
        self,
        db: Session,
        request: TripCreate,
    ) -> Trip:

        trip = Trip(**request.model_dump())

        return self.repository.create(db, trip)

    def update(
        self,
        db: Session,
        trip_id: int,
        request: TripUpdate,
    ) -> Trip:

        trip = self.get_by_id(db, trip_id)

        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(trip, key, value)

        return self.repository.update(db, trip)

    def delete(
        self,
        db: Session,
        trip_id: int,
    ) -> None:

        trip = self.get_by_id(db, trip_id)

        self.repository.delete(db, trip)