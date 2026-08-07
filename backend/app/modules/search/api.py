from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_trip_search_service
from app.modules.search.schemas import TripSearchResponse
from app.modules.search.service import TripSearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(
    "/trips",
    response_model=list[TripSearchResponse],
)
def search_trips(
    keyword: str,
    db: Session = Depends(get_db),
    service: TripSearchService = Depends(get_trip_search_service),
):
    return service.search_by_title(db, keyword)
