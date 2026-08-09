from sqlalchemy import select

from app.modules.user.models import User
from app.shared.query_builder import QueryBuilder


def test_query_builder_starts_from_existing_statement() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    assert builder.build() is stmt


def test_query_builder_where_adds_condition_and_returns_self() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.where(User.is_active.is_(True))

    assert result is builder
    assert builder.build() is not stmt

    compiled = builder.build().compile(compile_kwargs={"literal_binds": True})
    assert "WHERE" in str(compiled)
    assert "is_active" in str(compiled)


def test_query_builder_where_if_applies_condition_when_enabled() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.where_if(True, User.email == "user@example.com")

    assert result is builder
    compiled = builder.build().compile(compile_kwargs={"literal_binds": True})
    assert "WHERE" in str(compiled)
    assert "user@example.com" in str(compiled)


def test_query_builder_where_if_skips_condition_when_disabled() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.where_if(False, User.email == "user@example.com")

    assert result is builder
    assert builder.build() is stmt


def test_query_builder_order_by_adds_ordering_and_returns_self() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.order_by(User.email.asc())

    assert result is builder
    compiled = builder.build().compile(compile_kwargs={"literal_binds": True})
    assert "ORDER BY" in str(compiled)
    assert "email" in str(compiled)


def test_query_builder_order_by_if_uses_ascending_column_when_condition_is_true() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.order_by_if(True, User.email.asc(), User.full_name.desc())

    assert result is builder
    compiled = builder.build().compile(compile_kwargs={"literal_binds": True})
    assert "ORDER BY" in str(compiled)
    assert "email" in str(compiled)


def test_query_builder_order_by_if_uses_descending_column_when_condition_is_false() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.order_by_if(False, User.email.asc(), User.full_name.desc())

    assert result is builder
    compiled = builder.build().compile(compile_kwargs={"literal_binds": True})
    assert "ORDER BY" in str(compiled)
    assert "full_name" in str(compiled)


def test_query_builder_limit_and_offset_modify_statement() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.offset(5).limit(10)

    assert result is builder

    compiled = builder.build().compile(compile_kwargs={"literal_binds": True})
    assert "OFFSET 5" in str(compiled)
    assert "LIMIT 10" in str(compiled)


def test_query_builder_options_returns_self_and_preserves_statement() -> None:
    stmt = select(User)
    builder = QueryBuilder(stmt)

    result = builder.options()

    assert result is builder
    assert builder.build() is not None
    assert builder.build().compare(stmt)
