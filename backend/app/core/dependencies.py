from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.database.session import get_db

from app.modules.destination.repository import DestinationRepository
from app.modules.destination.service import DestinationService

from app.modules.trip.repository import TripRepository
from app.modules.trip.service import TripService

from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService

def get_destination_service(
    db: Session = Depends(get_db),
):
    repository = DestinationRepository()
    return DestinationService(repository)


def get_trip_service(
    db: Session = Depends(get_db),
):
    repository = TripRepository()
    return TripService(repository)

def get_user_service(
    db: Session = Depends(get_db),
):
    repository = UserRepository()
    return UserService(repository)