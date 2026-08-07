from fastapi import Depends

from app.modules.itinerary.repository import (
    ItineraryActivityRepository,
    ItineraryRepository,
    itinerary_activity_repository,
    itinerary_repository,
)
from app.modules.itinerary.service import (
    ItineraryActivityService,
    ItineraryService,
)


def get_itinerary_repository() -> ItineraryRepository:
    return itinerary_repository


def get_itinerary_activity_repository() -> ItineraryActivityRepository:
    return itinerary_activity_repository


def get_itinerary_service(
    repository: ItineraryRepository = Depends(
        get_itinerary_repository,
    ),
) -> ItineraryService:
    return ItineraryService(repository)


def get_itinerary_activity_service(
    repository: ItineraryActivityRepository = Depends(
        get_itinerary_activity_repository,
    ),
) -> ItineraryActivityService:
    return ItineraryActivityService(repository)