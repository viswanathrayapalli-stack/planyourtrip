from sqlalchemy.orm import Session

from app.modules.trip.constants import TRIP_NOT_FOUND
from app.modules.trip.models import Trip
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import (
    AuthorizationException,
    ResourceNotFoundException,
)
from app.shared.constants import FORBIDDEN


class AuthorizationService:

    def __init__(self, trip_repository: TripRepository):
        self.trip_repository = trip_repository

    def ensure_trip_owner(
        self,
        db: Session,
        trip_id: int,
        current_user_id: int,
    ) -> Trip:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException(TRIP_NOT_FOUND)

        if trip.user_id != current_user_id:
            raise AuthorizationException(FORBIDDEN)

        return trip