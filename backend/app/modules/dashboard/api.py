from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user,
    get_dashboard_service,
    get_db,
)
from app.modules.dashboard.schemas import DashboardResponse
from app.modules.dashboard.service import DashboardService
from app.modules.user.models import User


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/{trip_id}", response_model=DashboardResponse)
def get_dashboard(
    trip_id: int,
    db: Session = Depends(get_db),
    service: DashboardService = Depends(get_dashboard_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_dashboard(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
    )
