from sqlalchemy.orm import Session

from app.modules.checklist.constants import CHECKLIST_NOT_FOUND
from app.modules.checklist.models import Checklist
from app.modules.checklist.repository import ChecklistRepository
from app.modules.checklist.schemas import ChecklistCreate, ChecklistUpdate
from app.shared.authorization import AuthorizationService
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException


class ChecklistService:

    def __init__(
        self,
        repository: ChecklistRepository,
        trip_repository: TripRepository,
        authorization_service: AuthorizationService,
    ):
        self.repository = repository
        self.trip_repository = trip_repository
        self.authorization_service = authorization_service

    def get_all(
        self,
        db: Session,
    ) -> list[Checklist]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        checklist_id: int,
        user_id: int,
    ) -> Checklist:
        checklist = self.repository.get_by_id(db, checklist_id)

        if checklist is None:
            raise ResourceNotFoundException(CHECKLIST_NOT_FOUND)

        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=checklist.trip_id,
            current_user_id=user_id,
        )

        return checklist

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> list[Checklist]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        return self.repository.get_by_trip_id(db, trip_id)

    def create(
        self,
        db: Session,
        request: ChecklistCreate,
        user_id: int,
    ) -> Checklist:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=request.trip_id,
            current_user_id=user_id,
        )

        checklist = Checklist(**request.model_dump())

        return self.repository.create(db, checklist)

    def update(
        self,
        db: Session,
        checklist_id: int,
        request: ChecklistUpdate,
        user_id: int,
    ) -> Checklist:
        checklist = self.get_by_id(db, checklist_id, user_id)
        update_data = request.model_dump(exclude_unset=True)


        for key, value in update_data.items():
            setattr(checklist, key, value)

        return self.repository.update(db, checklist)

    def delete(
        self,
        db: Session,
        checklist_id: int,
        user_id: int,
    ) -> None:
        checklist = self.get_by_id(db, checklist_id, user_id)
        self.repository.delete(db, checklist)
