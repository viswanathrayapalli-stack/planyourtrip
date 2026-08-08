from sqlalchemy.orm import Session

from app.modules.expense.constants import EXPENSE_NOT_FOUND
from app.modules.expense.models import Expense
from app.modules.expense.repository import ExpenseRepository
from app.modules.expense.schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.shared.authorization import AuthorizationService
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException
from app.shared.pagination import PageResponse, PaginationParams


class ExpenseService:

    def __init__(
        self,
        repository: ExpenseRepository,
        trip_repository: TripRepository,
        authorization_service: AuthorizationService,
    ):
        self.repository = repository
        self.trip_repository = trip_repository
        self.authorization_service = authorization_service

    def get_all(
        self,
        db: Session,
    ) -> list[Expense]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        expense_id: int,
        user_id: int,
    ) -> Expense:
        expense = self.repository.get_by_id(db, expense_id)

        if expense is None:
            raise ResourceNotFoundException(EXPENSE_NOT_FOUND)

        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=expense.trip_id,
            current_user_id=user_id,
        )

        return expense

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> list[Expense]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        return self.repository.get_by_trip_id(db, trip_id)

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[ExpenseResponse]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        page = self.repository.get_by_trip_id_paginated(
            db=db,
            trip_id=trip_id,
            pagination=pagination,
        )

        return PageResponse(
            items=[ExpenseResponse.model_validate(expense) for expense in page.items],
            total=page.total,
            page=page.page,
            page_size=page.page_size,
            total_pages=page.total_pages,
        )

    def create(
        self,
        db: Session,
        request: ExpenseCreate,
        user_id: int,
    ) -> Expense:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=request.trip_id,
            current_user_id=user_id,
        )

        expense = Expense(**request.model_dump())

        return self.repository.create(db, expense)

    def update(
        self,
        db: Session,
        expense_id: int,
        request: ExpenseUpdate,
        user_id: int,
    ) -> Expense:
        expense = self.get_by_id(db, expense_id, user_id)
        update_data = request.model_dump(exclude_unset=True)



        for key, value in update_data.items():
            setattr(expense, key, value)

        return self.repository.update(db, expense)

    def delete(
        self,
        db: Session,
        expense_id: int,
        user_id: int,
    ) -> None:
        expense = self.get_by_id(db, expense_id, user_id)
        self.repository.delete(db, expense)
