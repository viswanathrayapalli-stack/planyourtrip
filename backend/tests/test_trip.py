from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import select

from app.core.dependencies import get_current_user, get_db, get_trip_service
from app.main import app
from app.modules.trip.models import Trip
from app.modules.trip.repository import TripRepository
from app.modules.trip.schemas import TripCreate, TripResponse, TripUpdate
from app.modules.trip.service import TripService
from app.shared.exceptions.exceptions import AuthorizationException
from app.shared.filtering import (
    SearchParams,
    SortOrder,
    SortParams,
    TripFilterParams,
)
from app.shared.pagination import PageResponse, PaginationParams

client = TestClient(app)


def test_trip_model_has_expected_configuration() -> None:
    trip = Trip(user_id=1, title="Weekend getaway", description="A short trip", is_active=True)

    assert Trip.__tablename__ == "trips"
    assert trip.user_id == 1
    assert trip.title == "Weekend getaway"
    assert trip.description == "A short trip"
    assert trip.is_active is True

    assert Trip.__table__.c.user_id.nullable is False
    assert Trip.__table__.c.title.nullable is False
    assert Trip.__table__.c.description.nullable is True
    assert Trip.__table__.c.is_active.nullable is False
    assert any(
        str(fk.target_fullname) == "users.id"
        for fk in Trip.__table__.c.user_id.foreign_keys
    )


def test_trip_create_schema_accepts_minimal_input_and_sets_default_is_active() -> None:
    request = TripCreate(title="Weekend getaway")

    assert request.title == "Weekend getaway"
    assert request.description is None
    assert request.is_active is True


def test_trip_create_schema_accepts_full_input() -> None:
    request = TripCreate(title="Weekend getaway", description="A short trip", is_active=False)

    assert request.title == "Weekend getaway"
    assert request.description == "A short trip"
    assert request.is_active is False


@pytest.mark.parametrize(
    ("title", "description"),
    [
        ("x" * 151, None),
        ("ok", "x" * 1001),
    ],
)
def test_trip_create_schema_rejects_values_outside_defined_limits(title: str, description: str | None) -> None:
    with pytest.raises(ValidationError):
        TripCreate(title=title, description=description)


@pytest.mark.parametrize(
    ("title", "description", "is_active"),
    [
        ("Updated title", None, None),
        (None, "Updated description", True),
        (None, None, False),
    ],
)
def test_trip_update_schema_accepts_valid_partial_updates(
    title: str | None,
    description: str | None,
    is_active: bool | None,
) -> None:
    request = TripUpdate(title=title, description=description, is_active=is_active)

    assert request.title == title
    assert request.description == description
    assert request.is_active == is_active


def test_trip_update_schema_allows_empty_payload() -> None:
    request = TripUpdate()

    assert request.title is None
    assert request.description is None
    assert request.is_active is None


@pytest.mark.parametrize(
    ("title", "description", "is_active"),
    [
        ("x" * 151, None, None),
        (None, "x" * 1001, None),
    ],
)
def test_trip_update_schema_rejects_values_outside_defined_limits(
    title: str | None,
    description: str | None,
    is_active: bool | None,
) -> None:
    with pytest.raises(ValidationError):
        TripUpdate(title=title, description=description, is_active=is_active)


def test_trip_response_model_builds_from_attributes() -> None:
    trip = SimpleNamespace(
        id=7,
        title="Weekend getaway",
        description="A short trip",
        is_active=True,
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 2),
    )

    response = TripResponse.model_validate(trip)

    assert response.id == 7
    assert response.title == "Weekend getaway"
    assert response.description == "A short trip"
    assert response.is_active is True
    assert response.created_at == datetime(2024, 1, 1)
    assert response.updated_at == datetime(2024, 1, 2)


def test_trip_repository_get_by_id_and_user_returns_matching_trip() -> None:
    db = Mock()
    expected_trip = Trip(user_id=1, title="Trip", description=None, is_active=True)
    db.scalar.return_value = expected_trip

    repository = TripRepository()
    result = repository.get_by_id_and_user(db, 10, 1)

    assert result is expected_trip
    db.scalar.assert_called_once()

    statement = db.scalar.call_args.args[0]
    assert statement is not None
    expected_statement = select(Trip).where(Trip.id == 10, Trip.user_id == 1)
    assert statement.compare(expected_statement)


def test_trip_repository_get_by_id_and_user_returns_none_when_missing() -> None:
    db = Mock()
    db.scalar.return_value = None

    repository = TripRepository()
    result = repository.get_by_id_and_user(db, 10, 1)

    assert result is None
    db.scalar.assert_called_once()


def test_trip_repository_get_all_by_user_returns_rows_for_user() -> None:
    db = Mock()
    expected_trips = [Trip(user_id=1, title="Trip", description=None, is_active=True)]
    db.scalars.return_value.all.return_value = expected_trips

    repository = TripRepository()
    result = repository.get_all_by_user(db, 1)

    assert result == expected_trips
    db.scalars.assert_called_once()

    statement = db.scalars.call_args.args[0]
    assert statement is not None
    expected_statement = select(Trip).where(Trip.user_id == 1)
    assert statement.compare(expected_statement)


def test_trip_repository_get_all_by_user_returns_empty_list_when_no_rows() -> None:
    db = Mock()
    db.scalars.return_value.all.return_value = []

    repository = TripRepository()
    result = repository.get_all_by_user(db, 1)

    assert result == []


def test_trip_repository_get_all_by_user_paginated_supports_search_sort_and_is_active_filter() -> None:
    db = Mock()
    expected_items = [Trip(user_id=7, title="Trip A", description="Alpha", is_active=True)]
    db.scalar.return_value = 5
    db.scalars.return_value.all.return_value = expected_items

    repository = TripRepository()
    pagination = PaginationParams(page=2, page_size=2)
    sort = SortParams(sort_by="title", sort_order=SortOrder.ASC)
    trip_filter = TripFilterParams(is_active=True)
    search = SearchParams(q="alpha")

    result = repository.get_all_by_user_paginated(
        db=db,
        user_id=7,
        pagination=pagination,
        sort=sort,
        trip_filter=trip_filter,
        search=search,
    )

    assert isinstance(result, PageResponse)
    assert result.total == 5
    assert result.page == 2
    assert result.page_size == 2
    assert result.total_pages == 3
    assert result.items == expected_items
    db.scalar.assert_called_once()
    db.scalars.assert_called_once()

    scalar_statement = db.scalar.call_args.args[0]
    scalars_statement = db.scalars.call_args.args[0]
    assert scalar_statement is not None
    assert scalars_statement is not None

    scalar_sql = str(scalar_statement.compile(compile_kwargs={"literal_binds": True}))
    scalars_sql = str(scalars_statement.compile(compile_kwargs={"literal_binds": True}))
    assert "user_id" in scalar_sql.lower()
    assert "order by" in scalars_sql.lower()
    assert "offset 2" in scalars_sql.lower()
    assert "limit 2" in scalars_sql.lower()
    assert "title" in scalars_sql.lower()
    assert "is_active" in scalars_sql.lower()
    assert "alpha" in scalars_sql.lower()
    assert "description" in scalars_sql.lower()


@pytest.mark.parametrize("is_active", [True, False])
def test_trip_repository_get_all_by_user_paginated_applies_explicit_is_active_filter(is_active: bool) -> None:
    db = Mock()
    db.scalar.return_value = 0
    db.scalars.return_value.all.return_value = []

    repository = TripRepository()
    pagination = PaginationParams(page=1, page_size=10)
    sort = SortParams(sort_by="unknown_field", sort_order=SortOrder.ASC)
    trip_filter = TripFilterParams(is_active=is_active)
    search = SearchParams(q=None)

    repository.get_all_by_user_paginated(
        db=db,
        user_id=7,
        pagination=pagination,
        sort=sort,
        trip_filter=trip_filter,
        search=search,
    )

    scalars_statement = db.scalars.call_args.args[0]
    assert scalars_statement is not None
    compiled_sql = str(scalars_statement.compile(compile_kwargs={"literal_binds": True}))
    assert "order by" in compiled_sql.lower()
    assert "created_at" in compiled_sql.lower()
    assert "desc" in compiled_sql.lower()
    assert "is_active" in compiled_sql.lower()
    assert str(is_active).lower() in compiled_sql.lower()


def test_trip_service_get_all_delegates_to_repository() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    expected_trips = [Trip(user_id=1, title="Trip", description=None, is_active=True)]
    repository.get_all_by_user.return_value = expected_trips

    result = service.get_all(db, 7)

    assert result is expected_trips
    repository.get_all_by_user.assert_called_once_with(db, 7)


def test_trip_service_get_all_paginated_converts_items_to_trip_response() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    pagination = PaginationParams(page=1, page_size=10)
    sort = SortParams(sort_by="title", sort_order=SortOrder.ASC)
    trip_filter = TripFilterParams(is_active=None)
    search = SearchParams(q=None)
    trip = Trip(
        id=1,
        user_id=1,
        title="Trip",
        description=None,
        is_active=True,
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 2),
    )
    repository.get_all_by_user_paginated.return_value = SimpleNamespace(
        items=[trip],
        total=1,
        page=1,
        page_size=10,
        total_pages=1,
    )

    result = service.get_all_paginated(
        db=db,
        user_id=7,
        pagination=pagination,
        sort=sort,
        trip_filter=trip_filter,
        search=search,
    )

    assert result.total == 1
    assert result.page == 1
    assert result.page_size == 10
    assert result.total_pages == 1
    assert len(result.items) == 1
    assert isinstance(result.items[0], TripResponse)
    assert result.items[0].title == trip.title
    repository.get_all_by_user_paginated.assert_called_once_with(
        db=db,
        user_id=7,
        pagination=pagination,
        sort=sort,
        trip_filter=trip_filter,
        search=search,
    )


def test_trip_service_get_by_id_uses_authorization_service() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    expected_trip = Trip(user_id=1, title="Trip", description=None, is_active=True)
    authorization_service.ensure_trip_owner.return_value = expected_trip

    result = service.get_by_id(db, 10, 7)

    assert result is expected_trip
    authorization_service.ensure_trip_owner.assert_called_once_with(db=db, trip_id=10, current_user_id=7)


def test_trip_service_create_creates_trip_for_current_user() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    request = TripCreate(title="Trip", description=None, is_active=True)

    created_trip = Trip(user_id=1, title="Trip", description=None, is_active=True)
    repository.create.return_value = created_trip

    result = service.create(db, 7, request)

    assert result is created_trip
    repository.create.assert_called_once()
    authorization_service.ensure_trip_owner.assert_not_called()
    created_trip_arg = repository.create.call_args.args[1]
    assert isinstance(created_trip_arg, Trip)
    assert created_trip_arg.user_id == 7
    assert created_trip_arg.title == request.title
    assert created_trip_arg.is_active == request.is_active


def test_trip_service_update_updates_owned_trip() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    existing_trip = Trip(user_id=1, title="Old", description=None, is_active=True)
    authorization_service.ensure_trip_owner.return_value = existing_trip
    repository.update.return_value = existing_trip
    request = TripUpdate(title="New", is_active=False)

    result = service.update(db, 10, 7, request)

    assert result is existing_trip
    assert existing_trip.title == "New"
    assert existing_trip.is_active is False
    authorization_service.ensure_trip_owner.assert_called_once_with(
        db=db,
        trip_id=10,
        current_user_id=7,
    )
    repository.update.assert_called_once_with(db, existing_trip)


def test_trip_service_update_with_empty_request_leaves_trip_unchanged() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    existing_trip = Trip(user_id=1, title="Old", description="Keep me", is_active=True)
    authorization_service.ensure_trip_owner.return_value = existing_trip
    repository.update.return_value = existing_trip

    result = service.update(db, 10, 7, TripUpdate())

    assert result is existing_trip
    assert existing_trip.title == "Old"
    assert existing_trip.description == "Keep me"
    assert existing_trip.is_active is True
    authorization_service.ensure_trip_owner.assert_called_once_with(
        db=db,
        trip_id=10,
        current_user_id=7,
    )
    repository.update.assert_called_once_with(db, existing_trip)


def test_trip_service_delete_deletes_owned_trip() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    existing_trip = Trip(user_id=1, title="Old", description=None, is_active=True)
    authorization_service.ensure_trip_owner.return_value = existing_trip

    result = service.delete(db, 10, 7)

    assert result is None
    authorization_service.ensure_trip_owner.assert_called_once_with(
        db=db,
        trip_id=10,
        current_user_id=7,
    )
    repository.delete.assert_called_once_with(db, existing_trip)


def test_trip_service_delete_propagates_authorization_errors() -> None:
    repository = Mock()
    authorization_service = Mock()
    service = TripService(repository, authorization_service)
    db = object()
    authorization_service.ensure_trip_owner.side_effect = AuthorizationException("Forbidden")

    with pytest.raises(AuthorizationException):
        service.delete(db, 10, 7)

    repository.delete.assert_not_called()


class FakeTripService:
    def __init__(self) -> None:
        self.calls = []

    def get_all_paginated(self, **kwargs):
        self.calls.append(kwargs)
        return PageResponse(
            items=[TripResponse.model_validate(Trip(id=1, user_id=1, title="Trip", description=None, is_active=True, created_at=datetime(2024, 1, 1), updated_at=datetime(2024, 1, 2)))],
            total=1,
            page=1,
            page_size=10,
            total_pages=1,
        )

    def get_by_id(self, db, trip_id, user_id):
        self.calls.append({"db": db, "trip_id": trip_id, "user_id": user_id})
        return Trip(id=trip_id, user_id=user_id, title="Trip", description=None, is_active=True, created_at=datetime(2024, 1, 1), updated_at=datetime(2024, 1, 2))

    def create(self, db, user_id, request):
        self.calls.append({"db": db, "user_id": user_id, "request": request})
        return Trip(id=1, user_id=user_id, title=request.title, description=request.description, is_active=request.is_active, created_at=datetime(2024, 1, 1), updated_at=datetime(2024, 1, 2))

    def update(self, db, trip_id, user_id, request):
        self.calls.append({"db": db, "trip_id": trip_id, "user_id": user_id, "request": request})
        return Trip(id=trip_id, user_id=user_id, title=request.title or "Trip", description=request.description, is_active=request.is_active if request.is_active is not None else True, created_at=datetime(2024, 1, 1), updated_at=datetime(2024, 1, 2))

    def delete(self, db, trip_id, user_id):
        self.calls.append({"db": db, "trip_id": trip_id, "user_id": user_id})
        return None


def test_trip_list_endpoint_returns_paginated_response_for_authenticated_user() -> None:
    fake_service = FakeTripService()

    def fake_get_trip_service():
        return fake_service

    def fake_get_db():
        return object()

    def fake_get_current_user():
        return SimpleNamespace(id=7, is_active=True)

    app.dependency_overrides[get_trip_service] = fake_get_trip_service
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_get_current_user

    try:
        response = client.get(
            "/api/v1/trips",
            params={"page": 1, "page_size": 10},
        )
    finally:
        app.dependency_overrides.pop(get_trip_service, None)
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == status.HTTP_200_OK
    assert fake_service.calls[0]["user_id"] == 7
    assert fake_service.calls[0]["pagination"].page == 1
    assert fake_service.calls[0]["pagination"].page_size == 10
    assert "status_filter" not in fake_service.calls[0]
    assert "date_range" not in fake_service.calls[0]
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["title"] == "Trip"


def test_trip_detail_endpoint_uses_current_user_id() -> None:
    fake_service = FakeTripService()

    def fake_get_trip_service():
        return fake_service

    def fake_get_db():
        return object()

    def fake_get_current_user():
        return SimpleNamespace(id=7, is_active=True)

    app.dependency_overrides[get_trip_service] = fake_get_trip_service
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_get_current_user

    try:
        response = client.get("/api/v1/trips/10")
    finally:
        app.dependency_overrides.pop(get_trip_service, None)
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == status.HTTP_200_OK
    assert fake_service.calls[0]["user_id"] == 7
    assert fake_service.calls[0]["trip_id"] == 10


def test_trip_list_endpoint_requires_authentication() -> None:
    response = client.get("/api/v1/trips")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trip_create_endpoint_returns_created_trip() -> None:
    fake_service = FakeTripService()

    def fake_get_trip_service():
        return fake_service

    def fake_get_db():
        return object()

    def fake_get_current_user():
        return SimpleNamespace(id=7, is_active=True)

    app.dependency_overrides[get_trip_service] = fake_get_trip_service
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_get_current_user

    try:
        response = client.post(
            "/api/v1/trips",
            json={"title": "Trip", "description": "Test", "is_active": True},
        )
    finally:
        app.dependency_overrides.pop(get_trip_service, None)
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == status.HTTP_201_CREATED
    assert fake_service.calls[0]["user_id"] == 7
    assert fake_service.calls[0]["request"].title == "Trip"
    assert fake_service.calls[0]["request"].description == "Test"
    assert fake_service.calls[0]["request"].is_active is True
    assert response.json()["title"] == "Trip"


def test_trip_update_endpoint_uses_current_user_id() -> None:
    fake_service = FakeTripService()

    def fake_get_trip_service():
        return fake_service

    def fake_get_db():
        return object()

    def fake_get_current_user():
        return SimpleNamespace(id=7, is_active=True)

    app.dependency_overrides[get_trip_service] = fake_get_trip_service
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_get_current_user

    try:
        response = client.put(
            "/api/v1/trips/10",
            json={"title": "Updated trip"},
        )
    finally:
        app.dependency_overrides.pop(get_trip_service, None)
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == status.HTTP_200_OK
    assert fake_service.calls[0]["user_id"] == 7
    assert fake_service.calls[0]["trip_id"] == 10
    assert fake_service.calls[0]["request"].title == "Updated trip"


def test_trip_update_endpoint_requires_authentication() -> None:
    response = client.put(
        "/api/v1/trips/10",
        json={"title": "Updated trip"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trip_delete_endpoint_requires_authentication() -> None:
    response = client.delete("/api/v1/trips/10")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_trip_create_endpoint_rejects_invalid_title() -> None:
    fake_service = FakeTripService()

    def fake_get_trip_service():
        return fake_service

    def fake_get_db():
        return object()

    def fake_get_current_user():
        return SimpleNamespace(id=7, is_active=True)

    app.dependency_overrides[get_trip_service] = fake_get_trip_service
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_get_current_user

    try:
        response = client.post(
            "/api/v1/trips",
            json={"title": "x" * 151},
        )
    finally:
        app.dependency_overrides.pop(get_trip_service, None)
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert fake_service.calls == []


def test_trip_delete_endpoint_returns_no_content() -> None:
    fake_service = FakeTripService()

    def fake_get_trip_service():
        return fake_service

    def fake_get_db():
        return object()

    def fake_get_current_user():
        return SimpleNamespace(id=7, is_active=True)

    app.dependency_overrides[get_trip_service] = fake_get_trip_service
    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_get_current_user

    try:
        response = client.delete("/api/v1/trips/10")
    finally:
        app.dependency_overrides.pop(get_trip_service, None)
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert fake_service.calls[0]["user_id"] == 7
    assert fake_service.calls[0]["trip_id"] == 10
