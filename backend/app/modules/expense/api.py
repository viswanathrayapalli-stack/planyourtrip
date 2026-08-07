from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_expense_service
from app.modules.expense.schemas import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.modules.expense.service import ExpenseService


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
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
):
    return service.create(db, request)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_by_id(
    expense_id: int,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_by_id(db, expense_id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update(
    expense_id: int,
    request: ExpenseUpdate,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.update(db, expense_id, request)


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    expense_id: int,
    db: Session = Depends(get_db),
    service: ExpenseService = Depends(get_expense_service),
):
    service.delete(db, expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
