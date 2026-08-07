from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_note_service
from app.modules.note.schemas import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.modules.note.service import NoteService


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
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
):
    return service.create(db, request)


@router.get("/{note_id}", response_model=NoteResponse)
def get_by_id(
    note_id: int,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
):
    return service.get_by_id(db, note_id)


@router.put("/{note_id}", response_model=NoteResponse)
def update(
    note_id: int,
    request: NoteUpdate,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
):
    return service.update(db, note_id, request)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    note_id: int,
    db: Session = Depends(get_db),
    service: NoteService = Depends(get_note_service),
):
    service.delete(db, note_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
