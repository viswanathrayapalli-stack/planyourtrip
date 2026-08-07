from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_timeline_service
from app.modules.timeline.schemas import TimelineResponse
from app.modules.timeline.service import TimelineService


router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"],
)


@router.get("/trips/{trip_id}", response_model=TimelineResponse)
def get_timeline(
    trip_id: int,
    db: Session = Depends(get_db),
    service: TimelineService = Depends(get_timeline_service),
):
    return service.get_timeline(db, trip_id)
