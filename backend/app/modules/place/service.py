from sqlalchemy.orm import Session

from app.modules.place.constants import PLACE_NOT_FOUND
from app.modules.place.models import Place
from app.modules.place.repository import PlaceRepository
from app.modules.place.schemas import PlaceCreate, PlaceUpdate
from app.shared.exceptions.exceptions import ResourceNotFoundException


class PlaceService:

    def __init__(self, repository: PlaceRepository):
        self.repository = repository

    def create(self, db: Session, request: PlaceCreate) -> Place:
        place = Place(**request.model_dump())
        return self.repository.create(db, place)

    def get_by_id(self, db: Session, place_id: int) -> Place:
        place = self.repository.get_by_id(db, place_id)

        if place is None:
            raise ResourceNotFoundException(PLACE_NOT_FOUND)

        return place

    def get_all(self, db: Session) -> list[Place]:
        return self.repository.get_all(db)

    def get_by_destination_id(self, db: Session, destination_id: int) -> list[Place]:
        return self.repository.get_by_destination_id(db, destination_id)

    def get_destination(self, db: Session, place_id: int):
        place = self.get_by_id(db, place_id)
        return place.destination

    def update(self, db: Session, place_id: int, request: PlaceUpdate) -> Place:
        place = self.get_by_id(db, place_id)
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(place, key, value)

        return self.repository.update(db, place)

    def delete(self, db: Session, place_id: int) -> None:
        place = self.get_by_id(db, place_id)
        self.repository.delete(db, place)
