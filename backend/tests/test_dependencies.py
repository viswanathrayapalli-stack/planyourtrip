from unittest.mock import patch

from app.ai.providers import OpenAIProvider
from app.ai.providers.mock_provider import MockAIProvider
from app.ai.services import ItineraryAIService
from app.core import dependencies as core_dependencies
from app.core.health import HealthService
from app.modules.analytics.service import AnalyticsService
from app.modules.attachment.service import AttachmentService
from app.modules.booking.service import BookingService
from app.modules.checklist.service import ChecklistService
from app.modules.dashboard.service import DashboardService
from app.modules.destination.service import DestinationService
from app.modules.expense.service import ExpenseService
from app.modules.favorite.service import FavoriteService
from app.modules.note.service import NoteService
from app.modules.notification.service import NotificationService
from app.modules.place.service import PlaceService
from app.modules.recommendation.service import RecommendationService
from app.modules.search.service import TripSearchService
from app.modules.timeline.service import TimelineService
from app.modules.trip.service import TripService
from app.modules.trip_share.service import TripShareService
from app.modules.user.service import UserService
from app.shared.authorization import AuthorizationService
from app.shared.email import EmailService
from app.shared.storage.local_storage import LocalStorageService


def test_provider_construction_returns_expected_service_types() -> None:
    fake_db = object()

    place_service = core_dependencies.get_place_service(db=fake_db)
    assert isinstance(place_service, PlaceService)

    destination_service = core_dependencies.get_destination_service(
        db=fake_db,
        place_service=place_service,
    )
    assert isinstance(destination_service, DestinationService)

    authorization_service = core_dependencies.get_authorization_service()
    assert isinstance(authorization_service, AuthorizationService)

    trip_service = core_dependencies.get_trip_service(
        db=fake_db,
        authorization_service=authorization_service,
    )
    assert isinstance(trip_service, TripService)

    booking_service = core_dependencies.get_booking_service(
        authorization_service=authorization_service,
    )
    assert isinstance(booking_service, BookingService)

    expense_service = core_dependencies.get_expense_service(
        authorization_service=authorization_service,
    )
    assert isinstance(expense_service, ExpenseService)

    checklist_service = core_dependencies.get_checklist_service(
        authorization_service=authorization_service,
    )
    assert isinstance(checklist_service, ChecklistService)

    note_service = core_dependencies.get_note_service(
        authorization_service=authorization_service,
    )
    assert isinstance(note_service, NoteService)

    dashboard_service = core_dependencies.get_dashboard_service(
        authorization_service=authorization_service,
    )
    assert isinstance(dashboard_service, DashboardService)

    analytics_service = core_dependencies.get_analytics_service(
        authorization_service=authorization_service,
    )
    assert isinstance(analytics_service, AnalyticsService)

    timeline_service = core_dependencies.get_timeline_service(
        authorization_service=authorization_service,
    )
    assert isinstance(timeline_service, TimelineService)

    trip_search_service = core_dependencies.get_trip_search_service()
    assert isinstance(trip_search_service, TripSearchService)

    recommendation_service = core_dependencies.get_recommendation_service()
    assert isinstance(recommendation_service, RecommendationService)

    favorite_service = core_dependencies.get_favorite_service(
        authorization_service=authorization_service,
    )
    assert isinstance(favorite_service, FavoriteService)

    email_service = core_dependencies.get_email_service()
    assert isinstance(email_service, EmailService)

    trip_share_service = core_dependencies.get_trip_share_service(
        email_service=email_service,
    )
    assert isinstance(trip_share_service, TripShareService)

    attachment_service = core_dependencies.get_attachment_service(
        authorization_service=authorization_service,
        storage=core_dependencies.get_storage_service(),
    )
    assert isinstance(attachment_service, AttachmentService)

    notification_service = core_dependencies.get_notification_service()
    assert isinstance(notification_service, NotificationService)

    user_service = core_dependencies.get_user_service(db=fake_db)
    assert isinstance(user_service, UserService)


def test_get_health_service_returns_existing_health_service_instance() -> None:
    health_service = core_dependencies.get_health_service()

    assert isinstance(health_service, HealthService)
    assert health_service is core_dependencies.health_service


def test_get_ai_provider_returns_mock_provider_when_enabled() -> None:
    with patch.object(core_dependencies.settings, "AI_PROVIDER", "mock"):
        provider = core_dependencies.get_ai_provider()

    assert isinstance(provider, MockAIProvider)


def test_get_ai_provider_returns_openai_provider_when_not_mock() -> None:
    class FakeOpenAIProvider:
        pass

    with patch.object(core_dependencies.settings, "AI_PROVIDER", "openai"):
        with patch.object(core_dependencies, "OpenAIProvider", FakeOpenAIProvider):
            provider = core_dependencies.get_ai_provider()

    assert isinstance(provider, FakeOpenAIProvider)
    assert not isinstance(provider, MockAIProvider)


def test_get_itinerary_ai_service_returns_itinerary_ai_service() -> None:
    with patch.object(core_dependencies, "get_ai_provider", return_value=MockAIProvider()):
        itinerary_service = core_dependencies.get_itinerary_ai_service()

    assert isinstance(itinerary_service, ItineraryAIService)
    assert isinstance(itinerary_service.provider, MockAIProvider)


def test_get_storage_service_returns_local_storage_service() -> None:
    storage_service = core_dependencies.get_storage_service()

    assert isinstance(storage_service, LocalStorageService)
