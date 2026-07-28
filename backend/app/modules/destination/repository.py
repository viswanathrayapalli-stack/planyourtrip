from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.destination.models import Destination


class DestinationRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Destination]:
        stmt = select(Destination)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, destination_id: int) -> Destination | None:
        stmt = select(Destination).where(Destination.id == destination_id)
        return self.db.scalar(stmt)

    def get_by_name(self, name: str) -> Destination | None:
        stmt = select(Destination).where(Destination.name == name)
        return self.db.scalar(stmt)

    def create(self, destination: Destination) -> Destination:
        self.db.add(destination)
        self.db.commit()
        self.db.refresh(destination)
        return destination

    def update(self, destination: Destination) -> Destination:
        self.db.commit()
        self.db.refresh(destination)
        return destination

    def delete(self, destination: Destination) -> None:
        self.db.delete(destination)
        self.db.commit()