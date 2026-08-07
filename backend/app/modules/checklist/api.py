from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_checklist_service, get_db
from app.modules.checklist.schemas import (
    ChecklistCreate,
    ChecklistResponse,
    ChecklistUpdate,
)
from app.modules.checklist.service import ChecklistService


router = APIRouter(
    prefix="/checklists",
    tags=["Checklists"],
)


@router.get("", response_model=list[ChecklistResponse])
def get_all(
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
):
    return service.get_all(db)


@router.post(
    "",
    response_model=ChecklistResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: ChecklistCreate,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
):
    return service.create(db, request)


@router.get("/{checklist_id}", response_model=ChecklistResponse)
def get_by_id(
    checklist_id: int,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
):
    return service.get_by_id(db, checklist_id)


@router.put("/{checklist_id}", response_model=ChecklistResponse)
def update(
    checklist_id: int,
    request: ChecklistUpdate,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
):
    return service.update(db, checklist_id, request)


@router.delete(
    "/{checklist_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    checklist_id: int,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
):
    service.delete(db, checklist_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
