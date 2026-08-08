from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db, get_note_service
from app.modules.note.schemas import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.modules.note.service import NoteService
from app.modules.user.models import User
from app.shared.pagination import PageResponse, PaginationParams


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get(
    "/trips/{trip_id}",
    response_model=PageResponse[NoteResponse],
)
def get_by_trip_id(
    trip_id: int,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
):
    return service.get_by_trip_id_paginated(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
        pagination=pagination,
    )


@router.get("", response_model=list[NoteResponse])
def get_all(
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
):
    return service.get_all(db)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: NoteCreate,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db=db,
        request=request,
        user_id=current_user.id,
    )


@router.get("/{note_id}", response_model=NoteResponse)
def get_by_id(
    note_id: int,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(
        db=db,
        note_id=note_id,
        user_id=current_user.id,
    )


@router.put("/{note_id}", response_model=NoteResponse)
def update(
    note_id: int,
    request: NoteUpdate,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(
        db=db,
        note_id=note_id,
        request=request,
        user_id=current_user.id,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    note_id: int,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db=db,
        note_id=note_id,
        user_id=current_user.id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
