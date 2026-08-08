from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    get_db,
    get_booking_service,
)
from app.modules.booking.schemas import (
    BookingCreate,
    BookingResponse,
    BookingUpdate,
)
from app.modules.booking.service import BookingService
from app.modules.user.models import User
from app.shared.pagination import PageResponse, PaginationParams


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("/trips/{trip_id}", response_model=PageResponse[BookingResponse])
def get_by_trip_id(
    trip_id: int,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
):
    return service.get_by_trip_id_paginated(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
        pagination=pagination,
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
    current_user: User = Depends(get_current_user),
):
    return service.create(
        db=db,
        request=request,
        user_id=current_user.id,
    )


@router.get("/{booking_id}", response_model=BookingResponse)
def get_by_id(
    booking_id: int,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(
        db=db,
        booking_id=booking_id,
        user_id=current_user.id,
    )


@router.put("/{booking_id}", response_model=BookingResponse)
def update(
    booking_id: int,
    request: BookingUpdate,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    return service.update(
        db=db,
        booking_id=booking_id,
        request=request,
        user_id=current_user.id,
    )


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    booking_id: int,
    db: Session = Depends(get_db),
    service: BookingService = Depends(get_booking_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db=db,
        booking_id=booking_id,
        user_id=current_user.id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
