from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db, get_expense_service
from app.modules.expense.schemas import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.modules.expense.service import ExpenseService
from app.modules.user.models import User
from app.shared.pagination import PageResponse, PaginationParams


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.get("/trips/{trip_id}", response_model=PageResponse[ExpenseResponse])
def get_by_trip_id(
    trip_id: int,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
):
    return service.get_by_trip_id_paginated(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
        pagination=pagination,
    )


@router.get("", response_model=list[ExpenseResponse])
def get_all(
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_all(db)


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: ExpenseCreate,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db=db,
        request=request,
        user_id=current_user.id,
    )


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_by_id(
    expense_id: int,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(
        db=db,
        expense_id=expense_id,
        user_id=current_user.id,
    )


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update(
    expense_id: int,
    request: ExpenseUpdate,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(
        db=db,
        expense_id=expense_id,
        request=request,
        user_id=current_user.id,
    )


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    expense_id: int,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db=db,
        expense_id=expense_id,
        user_id=current_user.id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
