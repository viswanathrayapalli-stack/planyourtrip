from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.modules.trip.models import Trip
from app.shared.filtering import (
    SearchParams,
    SortOrder,
    SortParams,
    TripFilterParams,
)
from app.shared.query_builder import QueryBuilder
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.repositories import BaseRepository


class TripRepository(BaseRepository[Trip]):

    def __init__(self):
        super().__init__(Trip)

    def get_by_id_and_user(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> Trip | None:
        stmt = select(Trip).where(
            Trip.id == trip_id,
            Trip.user_id == user_id,
        )
        return db.scalar(stmt)

    def get_all_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Trip]:
        stmt = select(Trip).where(Trip.user_id == user_id)
        return list(db.scalars(stmt).all())

    def get_all_by_user_paginated(
        self,
        db: Session,
        user_id: int,
        pagination: PaginationParams,
        sort: SortParams,
        trip_filter: TripFilterParams,
        search: SearchParams,
    ) -> PageResponse[Trip]:
        builder = QueryBuilder(select(Trip).where(Trip.user_id == user_id))

        builder.where_if(
            trip_filter.is_active is not None,
            Trip.is_active == trip_filter.is_active,
        )

        builder.where_if(
            search.q,
            or_(
                Trip.title.ilike(f"%{search.q}%"),
                Trip.description.ilike(f"%{search.q}%"),
            ),
        )

        if sort.sort_by in {"created_at", "updated_at", "title"}:
            column = getattr(Trip, sort.sort_by)

            if sort.sort_order == SortOrder.ASC:
                builder.order_by(column.asc())
            else:
                builder.order_by(column.desc())
        else:
            builder.order_by(Trip.created_at.desc())

        stmt = builder.build()

        return self.paginate(
            db=db,
            stmt=stmt,
            pagination=pagination,
        )


trip_repository = TripRepository()