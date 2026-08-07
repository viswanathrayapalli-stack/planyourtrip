from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_trip_share_service
from app.modules.trip_share.schemas import TripShareCreate, TripShareResponse
from app.modules.trip_share.service import TripShareService

router = APIRouter(prefix="/trip-shares", tags=["Trip Shares"])


@router.get(
    "/trips/{trip_id}",
    response_model=list[TripShareResponse],
)
def get_trip_shares(
    trip_id: int,
    db: Session = Depends(get_db),
    service: TripShareService = Depends(get_trip_share_service),
):
    return service.get_by_trip_id(db, trip_id)


@router.post(
    "/",
    response_model=TripShareResponse,
)
def create_trip_share(
    request: TripShareCreate,
    db: Session = Depends(get_db),
    service: TripShareService = Depends(get_trip_share_service),
):
    return service.create(db, request)


@router.delete(
    "/{share_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_trip_share(
    share_id: int,
    db: Session = Depends(get_db),
    service: TripShareService = Depends(get_trip_share_service),
):
    service.delete(db, share_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
