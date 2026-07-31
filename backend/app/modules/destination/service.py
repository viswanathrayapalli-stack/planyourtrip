from sqlalchemy.orm import Session
from app.modules.destination.constants import (
    DESTINATION_ALREADY_EXISTS,
    DESTINATION_NOT_FOUND,
)
from app.modules.destination.models import Destination
from app.modules.destination.repository import DestinationRepository
from app.modules.destination.schemas import (
    DestinationCreate,
    DestinationUpdate,
)
from app.modules.place.service import PlaceService
from app.shared.exceptions.exceptions import (
    ResourceNotFoundException,
    ValidationException,
)


class DestinationService:

    def __init__(self, repository: DestinationRepository, place_service: PlaceService):
        self.repository = repository
        self.place_service = place_service


    def get_all(self, db: Session):
        return self.repository.get_all(db)

    def get_by_id(self, db: Session, destination_id: int,):
        destination = self.repository.get_by_id(db, destination_id)

        if destination is None:
            raise ResourceNotFoundException(DESTINATION_NOT_FOUND)

        return destination

    def get_places(self, db: Session, destination_id: int):
        self.get_by_id(db, destination_id)
        return self.place_service.get_by_destination_id(
            db,
            destination_id,
        )

    def create(self, db: Session, request: DestinationCreate):
        existing = self.repository.get_by_name(db, request.name)

        if existing:
            raise ValidationException(DESTINATION_ALREADY_EXISTS)

        destination = Destination(
            name=request.name,
            country=request.country,
            description=request.description,
        )

        return self.repository.create(db, destination)    

    def update(self, db: Session, destination_id: int, request: DestinationUpdate):
        destination = self.get_by_id(db, destination_id)

        if request.name is not None:
            existing = self.repository.get_by_name(db, request.name)
            
            if existing and existing.id != destination.id:
                raise ValidationException(DESTINATION_ALREADY_EXISTS)

            destination.name = request.name

        if request.country is not None:
            destination.country = request.country

        if request.description is not None:
            destination.description = request.description

        if request.is_active is not None:
            destination.is_active = request.is_active

        return self.repository.update(db, destination)

    def delete(self, db: Session, destination_id: int):
        destination = self.get_by_id(db, destination_id)
        self.repository.delete(db, destination)