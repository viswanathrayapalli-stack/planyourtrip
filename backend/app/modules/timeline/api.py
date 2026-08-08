from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db, get_timeline_service
from app.modules.timeline.schemas import TimelineResponse
from app.modules.timeline.service import TimelineService
from app.modules.user.models import User


router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"],
)


@router.get("/trips/{trip_id}", response_model=TimelineResponse)
def get_timeline(
    trip_id: int,
    db: Session = Depends(get_db),
    service: TimelineService = Depends(get_timeline_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_timeline(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
    )
