from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_place_service
from app.modules.place.schemas import (
    PlaceCreate,
    PlaceResponse,
    PlaceUpdate,
)
from app.modules.place.service import PlaceService

router = APIRouter(
    prefix="/places",
    tags=["Places"],
)


@router.get("", response_model=list[PlaceResponse])
def get_all(
    db: Session = Depends(get_db),
    service: PlaceService = Depends(get_place_service),
):
    return service.get_all(db)


@router.post(
    "",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: PlaceCreate,
    db: Session = Depends(get_db),
    service: PlaceService = Depends(get_place_service),
):
    return service.create(db, request)


@router.get("/{place_id}", response_model=PlaceResponse)
def get_by_id(
    place_id: int,
    db: Session = Depends(get_db),
    service: PlaceService = Depends(get_place_service),
):
    return service.get_by_id(db, place_id)


@router.put("/{place_id}", response_model=PlaceResponse)
def update(
    place_id: int,
    request: PlaceUpdate,
    db: Session = Depends(get_db),
    service: PlaceService = Depends(get_place_service),
):
    return service.update(db, place_id, request)


@router.delete(
    "/{place_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    place_id: int,
    db: Session = Depends(get_db),
    service: PlaceService = Depends(get_place_service),
):
    service.delete(db, place_id)
