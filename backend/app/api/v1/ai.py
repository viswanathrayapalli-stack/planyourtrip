from fastapi import APIRouter, Depends

from app.ai.schemas import ItineraryGenerateRequest, ItineraryGenerateResponse
from app.ai.services import ItineraryAIService
from app.core.dependencies import get_itinerary_ai_service


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/itinerary", response_model=ItineraryGenerateResponse)
def generate_itinerary(
    request: ItineraryGenerateRequest,
    service: ItineraryAIService = Depends(get_itinerary_ai_service),
):
    result = service.generate_itinerary(
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        budget=request.budget,
        travelers=request.travelers,
    )

    return ItineraryGenerateResponse(
        itinerary=result,
    )