from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.shared.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: type[ModelType]):
        self.model = model

    def get_all(
        self,
        db: Session,
    ) -> list[ModelType]:
        return db.scalars(select(self.model)).all()

    def get_by_id(
        self,
        db: Session,
        entity_id: int,
    ) -> ModelType | None:
        return db.get(self.model, entity_id)

    def create(
        self,
        db: Session,
        entity: ModelType,
    ) -> ModelType:

        db.add(entity)
        db.commit()
        db.refresh(entity)

        return entity

    def update(
        self,
        db: Session,
        entity: ModelType,
    ) -> ModelType:

        db.commit()
        db.refresh(entity)

        return entity

    def delete(
        self,
        db: Session,
        entity: ModelType,
    ) -> None:

        db.delete(entity)
        db.commit()