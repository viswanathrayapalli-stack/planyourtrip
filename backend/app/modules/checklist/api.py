from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_checklist_service,
    get_current_user,
    get_db,
)
from app.modules.checklist.schemas import (
    ChecklistCreate,
    ChecklistResponse,
    ChecklistUpdate,
)
from app.modules.checklist.service import ChecklistService
from app.modules.user.models import User
from app.shared.pagination import PageResponse, PaginationParams


router = APIRouter(
    prefix="/checklists",
    tags=["Checklists"],
)


@router.get(
    "/trips/{trip_id}",
    response_model=PageResponse[ChecklistResponse],
)
def get_by_trip_id(
    trip_id: int,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
):
    return service.get_by_trip_id_paginated(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
        pagination=pagination,
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
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db=db,
        request=request,
        user_id=current_user.id,
    )


@router.get("/{checklist_id}", response_model=ChecklistResponse)
def get_by_id(
    checklist_id: int,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(
        db=db,
        checklist_id=checklist_id,
        user_id=current_user.id,
    )


@router.put("/{checklist_id}", response_model=ChecklistResponse)
def update(
    checklist_id: int,
    request: ChecklistUpdate,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(
        db=db,
        checklist_id=checklist_id,
        request=request,
        user_id=current_user.id,
    )


@router.delete(
    "/{checklist_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    checklist_id: int,
    db: Session = Depends(get_db),
    service: ChecklistService = Depends(get_checklist_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db=db,
        checklist_id=checklist_id,
        user_id=current_user.id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
