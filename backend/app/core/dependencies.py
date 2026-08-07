from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.modules.destination.repository import DestinationRepository
from app.modules.destination.service import DestinationService
from app.modules.identity.constants import UNAUTHORIZED
from app.modules.place.repository import PlaceRepository
from app.modules.place.service import PlaceService
from app.modules.trip.repository import TripRepository, trip_repository
from app.modules.trip.service import TripService
from app.modules.booking.repository import booking_repository
from app.modules.booking.service import BookingService
from app.modules.checklist.repository import checklist_repository
from app.modules.checklist.service import ChecklistService
from app.modules.expense.repository import expense_repository
from app.modules.expense.service import ExpenseService
from app.modules.itinerary.repository import itinerary_repository
from app.modules.note.repository import note_repository
from app.modules.note.service import NoteService
from app.modules.dashboard.service import DashboardService
from app.modules.analytics.service import AnalyticsService
from app.modules.favorite.repository import favorite_repository
from app.modules.favorite.service import FavoriteService
from app.modules.recommendation.repository import recommendation_repository
from app.modules.recommendation.service import RecommendationService
from app.modules.search.repository import trip_search_repository
from app.modules.search.service import TripSearchService
from app.modules.timeline.service import TimelineService
from app.modules.trip_share.repository import trip_share_repository
from app.modules.trip_share.service import TripShareService
from app.modules.user.models import User
from app.modules.user.repository import UserRepository, user_repository
from app.modules.user.service import UserService
from app.shared.database.session import get_db
from app.shared.exceptions.exceptions import AuthenticationException


def get_place_service(
    db: Session = Depends(get_db),
):
    repository = PlaceRepository()
    return PlaceService(repository)


def get_destination_service(
    db: Session = Depends(get_db),
    place_service: PlaceService = Depends(get_place_service),
):
    repository = DestinationRepository()
    return DestinationService(
        repository,
        place_service,
    )


def get_trip_service(
    db: Session = Depends(get_db),
):
    repository = TripRepository()
    return TripService(repository)


def get_booking_service() -> BookingService:
    return BookingService(
        booking_repository,
        trip_repository,
    )


def get_expense_service() -> ExpenseService:
    return ExpenseService(
        expense_repository,
        trip_repository,
    )


def get_checklist_service() -> ChecklistService:
    return ChecklistService(
        checklist_repository,
        trip_repository,
    )


def get_note_service() -> NoteService:
    return NoteService(
        note_repository,
        trip_repository,
    )


def get_dashboard_service() -> DashboardService:
    return DashboardService(
        trip_repository,
        booking_repository,
        expense_repository,
        checklist_repository,
        note_repository,
        itinerary_repository,
    )


def get_analytics_service() -> AnalyticsService:
    return AnalyticsService(
        trip_repository,
        expense_repository,
        booking_repository,
        checklist_repository,
        note_repository,
        itinerary_repository,
    )


def get_timeline_service() -> TimelineService:
    return TimelineService(
        trip_repository,
        booking_repository,
        itinerary_repository,
        expense_repository,
        checklist_repository,
        note_repository,
    )


def get_trip_search_service() -> TripSearchService:
    return TripSearchService(
        trip_search_repository,
    )


def get_recommendation_service() -> RecommendationService:
    return RecommendationService(
        recommendation_repository,
        DestinationRepository(),
    )


def get_favorite_service() -> FavoriteService:
    return FavoriteService(
        favorite_repository,
        trip_repository,
        PlaceRepository(),
    )


def get_trip_share_service() -> TripShareService:
    return TripShareService(
        trip_share_repository,
        trip_repository,
        UserRepository(),
    )


def get_user_service(
    db: Session = Depends(get_db),
):
    repository = UserRepository()
    return UserService(repository)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/identity/login"
)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationException(UNAUTHORIZED)

    except JWTError as exc:
        raise AuthenticationException(UNAUTHORIZED) from exc

    user = user_repository.get_by_id(
        db=db,
        entity_id=int(user_id),
    )

    if user is None:
        raise AuthenticationException(UNAUTHORIZED)

    if not user.is_active:
        raise AuthenticationException(UNAUTHORIZED)

    return user