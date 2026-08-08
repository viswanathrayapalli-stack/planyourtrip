from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.expense.models import Expense
from app.shared.query_builder import QueryBuilder
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.repositories.base_repository import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):

    def __init__(self):
        super().__init__(Expense)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Expense]:
        stmt = (
            select(Expense)
            .where(Expense.trip_id == trip_id)
            .order_by(Expense.expense_date.asc())
        )

        return list(db.scalars(stmt).all())

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[Expense]:
        builder = QueryBuilder(
            select(Expense).where(Expense.trip_id == trip_id)
        )
        builder.order_by(Expense.expense_date.asc())

        stmt = builder.build()
        return self.paginate(
            db=db,
            stmt=stmt,
            pagination=pagination,
        )


expense_repository = ExpenseRepository()
