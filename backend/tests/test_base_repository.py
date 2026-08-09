from unittest.mock import Mock

from sqlalchemy import select

from app.modules.user.models import User
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.repositories import BaseRepository


def test_base_repository_get_all_returns_scalars_all_result_for_populated_rows() -> None:
    db = Mock()
    expected_users = [User(full_name="Jane Doe", email="jane@example.com", password_hash="hash")]
    db.scalars.return_value.all.return_value = expected_users

    repository = BaseRepository(User)
    result = repository.get_all(db)

    assert result is expected_users
    db.scalars.assert_called_once()

    statement = db.scalars.call_args.args[0]
    assert statement is not None
    assert statement.compare(select(User))


def test_base_repository_get_all_returns_scalars_all_result_for_empty_rows() -> None:
    db = Mock()
    db.scalars.return_value.all.return_value = []

    repository = BaseRepository(User)
    result = repository.get_all(db)

    assert result == []
    db.scalars.assert_called_once()

    statement = db.scalars.call_args.args[0]
    assert statement is not None
    assert statement.compare(select(User))


def test_base_repository_get_by_id_returns_existing_entity() -> None:
    db = Mock()
    expected_user = User(full_name="Jane Doe", email="jane@example.com", password_hash="hash")
    db.get.return_value = expected_user

    repository = BaseRepository(User)
    result = repository.get_by_id(db, 42)

    assert result is expected_user
    db.get.assert_called_once_with(User, 42)


def test_base_repository_get_by_id_returns_none_when_entity_missing() -> None:
    db = Mock()
    db.get.return_value = None

    repository = BaseRepository(User)
    result = repository.get_by_id(db, 42)

    assert result is None
    db.get.assert_called_once_with(User, 42)


def test_base_repository_paginate_returns_page_response_for_normal_page() -> None:
    db = Mock()
    pagination = PaginationParams(page=2, page_size=2)
    expected_items = [
        User(full_name="Jane Doe", email="jane@example.com", password_hash="hash"),
        User(full_name="John Doe", email="john@example.com", password_hash="hash"),
    ]
    db.scalar.return_value = 5
    db.scalars.return_value.all.return_value = expected_items

    repository = BaseRepository(User)
    response = repository.paginate(db, select(User), pagination)

    assert isinstance(response, PageResponse)
    assert response.items == expected_items
    assert response.total == 5
    assert response.page == 2
    assert response.page_size == 2
    assert response.total_pages == 3

    db.scalar.assert_called_once()
    db.scalars.assert_called_once()

    paginated_statement = db.scalars.call_args.args[0]
    assert paginated_statement is not None

    compiled = paginated_statement.compile(compile_kwargs={"literal_binds": True})
    assert "OFFSET 2" in str(compiled)
    assert "LIMIT 2" in str(compiled)


def test_base_repository_paginate_returns_single_page_for_empty_result() -> None:
    db = Mock()
    pagination = PaginationParams(page=1, page_size=2)
    db.scalar.return_value = 0
    db.scalars.return_value.all.return_value = []

    repository = BaseRepository(User)
    response = repository.paginate(db, select(User), pagination)

    assert response.items == []
    assert response.total == 0
    assert response.page == 1
    assert response.page_size == 2
    assert response.total_pages == 1


def test_base_repository_paginate_sets_total_pages_for_partial_final_page() -> None:
    db = Mock()
    pagination = PaginationParams(page=3, page_size=2)
    db.scalar.return_value = 5
    db.scalars.return_value.all.return_value = [
        User(full_name="Jane Doe", email="jane@example.com", password_hash="hash")
    ]

    repository = BaseRepository(User)
    response = repository.paginate(db, select(User), pagination)

    assert response.total == 5
    assert response.page == 3
    assert response.page_size == 2
    assert response.total_pages == 3


def test_base_repository_paginate_applies_offset_and_limit_to_statement() -> None:
    db = Mock()
    pagination = PaginationParams(page=2, page_size=3)
    db.scalar.return_value = 1
    db.scalars.return_value.all.return_value = []

    repository = BaseRepository(User)
    repository.paginate(db, select(User), pagination)

    paginated_statement = db.scalars.call_args.args[0]
    assert paginated_statement is not None

    compiled = paginated_statement.compile(compile_kwargs={"literal_binds": True})
    assert "OFFSET 3" in str(compiled)
    assert "LIMIT 3" in str(compiled)


def test_base_repository_create_adds_commits_refreshes_and_returns_entity() -> None:
    db = Mock()
    entity = User(full_name="Jane Doe", email="jane@example.com", password_hash="hash")

    repository = BaseRepository(User)
    result = repository.create(db, entity)

    assert result is entity
    db.add.assert_called_once_with(entity)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(entity)


def test_base_repository_update_commits_refreshes_and_returns_entity() -> None:
    db = Mock()
    entity = User(full_name="Jane Doe", email="jane@example.com", password_hash="hash")

    repository = BaseRepository(User)
    result = repository.update(db, entity)

    assert result is entity
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(entity)
    db.add.assert_not_called()


def test_base_repository_delete_deletes_commits_and_returns_none() -> None:
    db = Mock()
    entity = User(full_name="Jane Doe", email="jane@example.com", password_hash="hash")

    repository = BaseRepository(User)
    result = repository.delete(db, entity)

    assert result is None
    db.delete.assert_called_once_with(entity)
    db.commit.assert_called_once_with()
    db.refresh.assert_not_called()
