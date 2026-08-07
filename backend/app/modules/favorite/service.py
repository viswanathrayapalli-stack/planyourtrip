from sqlalchemy.orm import Session

from app.modules.favorite.repository import FavoriteRepository
from app.modules.favorite.schemas import FavoriteCreate, FavoriteResponse
from app.modules.place.repository import PlaceRepository
from app.modules.trip.constants import TRIP_NOT_FOUND
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException, ValidationException


class FavoriteService:

    def __init__(
        self,
        repository: FavoriteRepository,
        trip_repository: TripRepository,
        place_repository: PlaceRepository,
    ):
        self.repository = repository
        self.trip_repository = trip_repository
        self.place_repository = place_repository

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[FavoriteResponse]:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException(TRIP_NOT_FOUND)

        favorites = self.repository.get_by_trip_id(db, trip_id)

        response = []

        for favorite in favorites:
            place = self.place_repository.get_by_id(db, favorite.place_id)

            if place is None:
                raise ResourceNotFoundException("Place not found.")

            response.append(
                FavoriteResponse(
                    id=favorite.id,
                    trip_id=favorite.trip_id,
                    place_id=favorite.place_id,
                    place_name=place.name,
                    city=place.city,
                    country=place.country,
                    place_type=place.place_type,
                    created_at=favorite.created_at,
                )
            )

        return response

    def create(
        self,
        db: Session,
        request: FavoriteCreate,
    ) -> FavoriteResponse:
        trip = self.trip_repository.get_by_id(db, request.trip_id)

        if trip is None:
            raise ResourceNotFoundException(TRIP_NOT_FOUND)

        place = self.place_repository.get_by_id(db, request.place_id)

        if place is None:
            raise ResourceNotFoundException("Place not found.")

        existing_favorite = self.repository.get_by_trip_and_place(
            db,
            request.trip_id,
            request.place_id,
        )

        if existing_favorite is not None:
            raise ValidationException("Place is already added to favorites.")

        favorite = self.repository.model(**request.model_dump())
        favorite = self.repository.create(db, favorite)

        return FavoriteResponse(
            id=favorite.id,
            trip_id=favorite.trip_id,
            place_id=favorite.place_id,
            place_name=place.name,
            city=place.city,
            country=place.country,
            place_type=place.place_type,
            created_at=favorite.created_at,
        )

    def delete(
        self,
        db: Session,
        favorite_id: int,
    ) -> None:
        favorite = self.repository.get_by_id(db, favorite_id)

        if favorite is None:
            raise ResourceNotFoundException("Favorite not found.")

        self.repository.delete(db, favorite)
