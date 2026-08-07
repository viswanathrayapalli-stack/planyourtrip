from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.itinerary.dependencies import (
    get_itinerary_activity_service,
    get_itinerary_service,
)
from app.modules.itinerary.schemas import (
    ItineraryActivityCreate,
    ItineraryActivityResponse,
    ItineraryActivityUpdate,
    ItineraryCreate,
    ItineraryResponse,
    ItineraryUpdate,
)
from app.modules.itinerary.service import (
    ItineraryActivityService,
    ItineraryService,
)

router = APIRouter(
    tags=["Itineraries"],
)


# ------------------------------------------------------------------
# Itineraries
# ------------------------------------------------------------------

@router.get(
    "/trips/{trip_id}/itineraries",
    response_model=list[ItineraryResponse],
)
def get_itineraries(
    trip_id: int,
    db: Session = Depends(get_db),
    service: ItineraryService = Depends(get_itinerary_service),
):
    return service.get_all(db, trip_id)


@router.get(
    "/itineraries/{itinerary_id}",
    response_model=ItineraryResponse,
)
def get_itinerary(
    itinerary_id: int,
    db: Session = Depends(get_db),
    service: ItineraryService = Depends(get_itinerary_service),
):
    return service.get_by_id(db, itinerary_id)


@router.post(
    "/trips/{trip_id}/itineraries",
    response_model=ItineraryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_itinerary(
    trip_id: int,
    request: ItineraryCreate,
    db: Session = Depends(get_db),
    service: ItineraryService = Depends(get_itinerary_service),
):
    request.trip_id = trip_id
    return service.create(db, request)


@router.put(
    "/itineraries/{itinerary_id}",
    response_model=ItineraryResponse,
)
def update_itinerary(
    itinerary_id: int,
    request: ItineraryUpdate,
    db: Session = Depends(get_db),
    service: ItineraryService = Depends(get_itinerary_service),
):
    return service.update(
        db,
        itinerary_id,
        request,
    )


@router.delete(
    "/itineraries/{itinerary_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_itinerary(
    itinerary_id: int,
    db: Session = Depends(get_db),
    service: ItineraryService = Depends(get_itinerary_service),
):
    service.delete(
        db,
        itinerary_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ------------------------------------------------------------------
# Activities
# ------------------------------------------------------------------

@router.get(
    "/itineraries/{itinerary_id}/activities",
    response_model=list[ItineraryActivityResponse],
)
def get_activities(
    itinerary_id: int,
    db: Session = Depends(get_db),
    service: ItineraryActivityService = Depends(
        get_itinerary_activity_service,
    ),
):
    return service.get_all(
        db,
        itinerary_id,
    )


@router.get(
    "/activities/{activity_id}",
    response_model=ItineraryActivityResponse,
)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    service: ItineraryActivityService = Depends(
        get_itinerary_activity_service,
    ),
):
    return service.get_by_id(
        db,
        activity_id,
    )


@router.post(
    "/itineraries/{itinerary_id}/activities",
    response_model=ItineraryActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_activity(
    itinerary_id: int,
    request: ItineraryActivityCreate,
    db: Session = Depends(get_db),
    service: ItineraryActivityService = Depends(
        get_itinerary_activity_service,
    ),
):
    request.itinerary_id = itinerary_id

    return service.create(
        db,
        request,
    )


@router.put(
    "/activities/{activity_id}",
    response_model=ItineraryActivityResponse,
)
def update_activity(
    activity_id: int,
    request: ItineraryActivityUpdate,
    db: Session = Depends(get_db),
    service: ItineraryActivityService = Depends(
        get_itinerary_activity_service,
    ),
):
    return service.update(
        db,
        activity_id,
        request,
    )


@router.delete(
    "/activities/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    service: ItineraryActivityService = Depends(
        get_itinerary_activity_service,
    ),
):
    service.delete(
        db,
        activity_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)