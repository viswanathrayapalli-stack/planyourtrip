from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.place.models import Place


class PlaceRepository:

    def create(self, db: Session, place: Place) -> Place:
        db.add(place)
        db.commit()
        db.refresh(place)
        return place

    def get_by_id(self, db: Session, place_id: int) -> Place | None:
        stmt = select(Place).where(Place.id == place_id)
        return db.scalar(stmt)

    def get_all(self, db: Session) -> list[Place]:
        stmt = select(Place)
        return list(db.scalars(stmt).all())

    def update(self, db: Session, place: Place) -> Place:
        db.commit()
        db.refresh(place)
        return place

    def delete(self, db: Session, place: Place) -> None:
        db.delete(place)
        db.commit()
