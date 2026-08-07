from sqlalchemy.orm import Session

from app.modules.destination.constants import DESTINATION_NOT_FOUND
from app.modules.destination.repository import DestinationRepository
from app.modules.recommendation.repository import RecommendationRepository
from app.modules.recommendation.schemas import RecommendedPlace, RecommendationResponse
from app.shared.exceptions.exceptions import ResourceNotFoundException


class RecommendationService:

    def __init__(
        self,
        repository: RecommendationRepository,
        destination_repository: DestinationRepository,
    ):
        self.repository = repository
        self.destination_repository = destination_repository

    def get_recommendations(
        self,
        db: Session,
        destination_id: int,
    ) -> RecommendationResponse:
        destination = self.destination_repository.get_by_id(db, destination_id)

        if destination is None:
            raise ResourceNotFoundException(DESTINATION_NOT_FOUND)

        places = self.repository.get_by_destination_id(db, destination_id)

        recommendations = [
            RecommendedPlace(
                id=place.id,
                name=place.name,
                city=place.city,
                state=place.state,
                country=place.country,
                place_type=place.place_type,
                description=place.description,
            )
            for place in places
        ]

        return RecommendationResponse(
            destination_id=destination.id,
            destination_name=destination.name,
            total_recommendations=len(recommendations),
            recommendations=recommendations,
        )
