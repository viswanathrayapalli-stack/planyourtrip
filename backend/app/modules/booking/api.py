from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_booking_service,
)
from app.modules.booking.schemas import (
    BookingCreate,
    BookingResponse,
    BookingUpdate,
)
from app.modules.booking.service import BookingService


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("", response_model=list[BookingResponse])
def get_all(
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
):
    return service.get_all(db)


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: BookingCreate,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
):
    return service.create(db, request)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_by_id(
    booking_id: int,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
):
    return service.get_by_id(db, booking_id)


@router.put("/{booking_id}", response_model=BookingResponse)
def update(
    booking_id: int,
    request: BookingUpdate,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
):
    return service.update(db, booking_id, request)


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    booking_id: int,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
):
    service.delete(db, booking_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
