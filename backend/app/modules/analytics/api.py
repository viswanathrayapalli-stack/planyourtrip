from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_analytics_service, get_db
from app.modules.analytics.schemas import BudgetSummaryResponse, TripProgressResponse
from app.modules.analytics.service import AnalyticsService


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/trips/{trip_id}/budget", response_model=BudgetSummaryResponse)
def get_budget_summary(
    trip_id: int,
    db: Session = Depends(get_db),
    service: AnalyticsService = Depends(get_analytics_service),
):
    return service.get_budget_summary(db, trip_id)


@router.get("/trips/{trip_id}/progress", response_model=TripProgressResponse)
def get_trip_progress(
    trip_id: int,
    db: Session = Depends(get_db),
    service: AnalyticsService = Depends(get_analytics_service),
):
    return service.get_trip_progress(db, trip_id)
