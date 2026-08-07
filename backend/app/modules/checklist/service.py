from sqlalchemy.orm import Session

from app.modules.checklist.constants import CHECKLIST_NOT_FOUND
from app.modules.checklist.models import Checklist
from app.modules.checklist.repository import ChecklistRepository
from app.modules.checklist.schemas import ChecklistCreate, ChecklistUpdate
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException


class ChecklistService:

    def __init__(
        self,
        repository: ChecklistRepository,
        trip_repository: TripRepository,
    ):
        self.repository = repository
        self.trip_repository = trip_repository

    def get_all(
        self,
        db: Session,
    ) -> list[Checklist]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        checklist_id: int,
    ) -> Checklist:
        checklist = self.repository.get_by_id(db, checklist_id)

        if checklist is None:
            raise ResourceNotFoundException(CHECKLIST_NOT_FOUND)

        return checklist

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Checklist]:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        return self.repository.get_by_trip_id(db, trip_id)

    def create(
        self,
        db: Session,
        request: ChecklistCreate,
    ) -> Checklist:
        trip = self.trip_repository.get_by_id(db, request.trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        checklist = Checklist(**request.model_dump())

        return self.repository.create(db, checklist)

    def update(
        self,
        db: Session,
        checklist_id: int,
        request: ChecklistUpdate,
    ) -> Checklist:
        checklist = self.get_by_id(db, checklist_id)
        update_data = request.model_dump(exclude_unset=True)


        for key, value in update_data.items():
            setattr(checklist, key, value)

        return self.repository.update(db, checklist)

    def delete(
        self,
        db: Session,
        checklist_id: int,
    ) -> None:
        checklist = self.get_by_id(db, checklist_id)
        self.repository.delete(db, checklist)
