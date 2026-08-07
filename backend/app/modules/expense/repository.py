from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.expense.models import Expense
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


expense_repository = ExpenseRepository()
