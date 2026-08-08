from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_analytics_service, get_current_user, get_db
from app.modules.analytics.schemas import BudgetSummaryResponse, TripProgressResponse
from app.modules.analytics.service import AnalyticsService
from app.modules.user.models import User


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/trips/{trip_id}/budget", response_model=BudgetSummaryResponse)
def get_budget_summary(
    trip_id: int,
    db: Session = Depends(get_db),
    service: AnalyticsService = Depends(get_analytics_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_budget_summary(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
    )


@router.get("/trips/{trip_id}/progress", response_model=TripProgressResponse)
def get_trip_progress(
    trip_id: int,
    db: Session = Depends(get_db),
    service: AnalyticsService = Depends(get_analytics_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_trip_progress(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
    )
