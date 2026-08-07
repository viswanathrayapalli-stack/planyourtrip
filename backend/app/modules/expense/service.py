from sqlalchemy.orm import Session

from app.modules.expense.constants import EXPENSE_NOT_FOUND
from app.modules.expense.models import Expense
from app.modules.expense.repository import ExpenseRepository
from app.modules.expense.schemas import ExpenseCreate, ExpenseUpdate
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException


class ExpenseService:

    def __init__(
        self,
        repository: ExpenseRepository,
        trip_repository: TripRepository,
    ):
        self.repository = repository
        self.trip_repository = trip_repository

    def get_all(
        self,
        db: Session,
    ) -> list[Expense]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        expense_id: int,
    ) -> Expense:
        expense = self.repository.get_by_id(db, expense_id)

        if expense is None:
            raise ResourceNotFoundException(EXPENSE_NOT_FOUND)

        return expense

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Expense]:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        return self.repository.get_by_trip_id(db, trip_id)

    def create(
        self,
        db: Session,
        request: ExpenseCreate,
    ) -> Expense:
        trip = self.trip_repository.get_by_id(db, request.trip_id)

        if trip is None:
            raise ResourceNotFoundException("Trip not found.")

        expense = Expense(**request.model_dump())

        return self.repository.create(db, expense)

    def update(
        self,
        db: Session,
        expense_id: int,
        request: ExpenseUpdate,
    ) -> Expense:
        expense = self.get_by_id(db, expense_id)
        update_data = request.model_dump(exclude_unset=True)



        for key, value in update_data.items():
            setattr(expense, key, value)

        return self.repository.update(db, expense)

    def delete(
        self,
        db: Session,
        expense_id: int,
    ) -> None:
        expense = self.get_by_id(db, expense_id)
        self.repository.delete(db, expense)
