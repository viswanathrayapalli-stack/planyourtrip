from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_trip_service
from app.modules.trip.schemas import (
    TripCreate,
    TripResponse,
    TripUpdate,
)
from app.modules.trip.service import TripService

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get(
    "",
    response_model=list[TripResponse],
)
def get_all(
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
):
    return service.get_all(db)


@router.get(
    "/{trip_id}",
    response_model=TripResponse,
)
def get_by_id(
    trip_id: int,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
):
    return service.get_by_id(db, trip_id)


@router.post(
    "",
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: TripCreate,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
):
    return service.create(db, request)


@router.put(
    "/{trip_id}",
    response_model=TripResponse,
)
def update(
    trip_id: int,
    request: TripUpdate,
    db: Session = Depends(get_db),
    service: TripService = Depends(get_trip_service),
):
    return service.update(
        db=db,
        trip_id=trip_id,
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
):
    service.delete(db, trip_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)