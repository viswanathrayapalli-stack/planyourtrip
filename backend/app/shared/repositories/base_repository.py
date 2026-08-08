import math
from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.shared.database.base import Base
from app.shared.pagination import PageResponse, PaginationParams

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

    def paginate(
        self,
        db: Session,
        stmt,
        pagination: PaginationParams,
    ) -> PageResponse[ModelType]:
        total = db.scalar(
            select(func.count()).select_from(stmt.subquery())
        ) or 0
        paginated_stmt = stmt.offset(pagination.offset).limit(pagination.page_size)
        items = list(db.scalars(paginated_stmt).all())
        total_pages = max(
            1,
            math.ceil(total / pagination.page_size),
        )

        return PageResponse(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages,
        )

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