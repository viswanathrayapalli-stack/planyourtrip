from sqlalchemy.orm import Session

from app.modules.place.models import Place
from app.modules.place.repository import PlaceRepository
from app.modules.place.schemas import PlaceCreate, PlaceUpdate


class PlaceService:

    def __init__(self):
        self.repository = PlaceRepository()

    def create(self, db: Session, request: PlaceCreate) -> Place:
        place = Place(**request.model_dump())
        return self.repository.create(db, place)

    def get_by_id(self, db: Session, place_id: int) -> Place | None:
        return self.repository.get_by_id(db, place_id)

    def get_all(self, db: Session) -> list[Place]:
        return self.repository.get_all(db)

    def update(self, db: Session, place: Place, request: PlaceUpdate) -> Place:
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(place, key, value)

        return self.repository.update(db, place)

    def delete(self, db: Session, place: Place) -> None:
        self.repository.delete(db, place)
