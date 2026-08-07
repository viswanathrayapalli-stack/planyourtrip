from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_recommendation_service
from app.modules.recommendation.schemas import RecommendationResponse
from app.modules.recommendation.service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get(
    "/destinations/{destination_id}",
    response_model=RecommendationResponse,
)
def get_recommendations(
    destination_id: int,
    db: Session = Depends(get_db),
    service: RecommendationService = Depends(get_recommendation_service),
):
    return service.get_recommendations(db, destination_id)
