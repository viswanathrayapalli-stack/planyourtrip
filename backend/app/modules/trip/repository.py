from sqlalchemy.orm import Session

from app.modules.trip.models import Trip
from app.shared.repositories import BaseRepository


class TripRepository(BaseRepository[Trip]):

    def __init__(self):
        super().__init__(Trip)


trip_repository = TripRepository()