from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.itinerary.models import Itinerary, ItineraryActivity
from app.shared.repositories import BaseRepository


class ItineraryRepository(BaseRepository[Itinerary]):

    def __init__(self):
        super().__init__(Itinerary)

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[Itinerary]:
        stmt = select(Itinerary).where(Itinerary.trip_id == trip_id).order_by(Itinerary.day_number.asc())
        return list(db.scalars(stmt).all())


itinerary_repository = ItineraryRepository()


class ItineraryActivityRepository(BaseRepository[ItineraryActivity]):

    def __init__(self):
        super().__init__(ItineraryActivity)

    def get_by_itinerary_id(
        self,
        db: Session,
        itinerary_id: int,
    ) -> list[ItineraryActivity]:
        stmt = select(ItineraryActivity).where(
            ItineraryActivity.itinerary_id == itinerary_id,
        ).order_by(ItineraryActivity.activity_order.asc())
        return list(db.scalars(stmt).all())


itinerary_activity_repository = ItineraryActivityRepository()