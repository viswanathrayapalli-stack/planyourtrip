from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db, get_trip_service
from app.modules.trip.schemas import (
    TripCreate,
    TripResponse,
    TripUpdate,
)
from app.modules.trip.service import TripService
from app.modules.user.models import User
from app.shared.pagination import PageResponse, PaginationParams

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get(
    "",
    response_model=PageResponse[TripResponse],
)
def get_all(
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
):
    return service.get_all_paginated(
        db=db,
        user_id=current_user.id,
        pagination=pagination,
    )


@router.get(
    "/{trip_id}",
    response_model=TripResponse,
)
def get_by_id(
    trip_id: int,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(db, trip_id, current_user.id)


@router.post(
    "",
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: TripCreate,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    current_user: User = Depends(get_current_user),
):
    return service.create(db, current_user.id, request)


@router.put(
    "/{trip_id}",
    response_model=TripResponse,
)
def update(
    trip_id: int,
    request: TripUpdate,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
        request=request,
    )


@router.delete(
    "/{trip_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    trip_id: int,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)