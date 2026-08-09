import pytest
from pydantic import ValidationError

from app.shared.pagination import PageResponse, PaginationParams


def test_pagination_params_uses_default_values() -> None:
    params = PaginationParams()

    assert params.page == 1
    assert params.page_size == 20


@pytest.mark.parametrize(
    ("page", "page_size"),
    [
        (1, 1),
        (1, 20),
        (1, 100),
        (10, 1),
        (10, 100),
    ],
)
def test_pagination_params_accepts_valid_boundary_values(page: int, page_size: int) -> None:
    params = PaginationParams(page=page, page_size=page_size)

    assert params.page == page
    assert params.page_size == page_size


@pytest.mark.parametrize(
    ("page", "page_size"),
    [
        (0, 20),
        (1, 0),
        (-1, 20),
        (1, 101),
        (0, 0),
    ],
)
def test_pagination_params_rejects_invalid_values(page: int, page_size: int) -> None:
    with pytest.raises(ValidationError):
        PaginationParams(page=page, page_size=page_size)


@pytest.mark.parametrize(
    ("page", "page_size", "expected_offset"),
    [
        (1, 20, 0),
        (2, 20, 20),
        (3, 10, 20),
    ],
)
def test_pagination_params_offset_is_calculated_from_page_and_page_size(
    page: int,
    page_size: int,
    expected_offset: int,
) -> None:
    params = PaginationParams(page=page, page_size=page_size)

    assert params.offset == expected_offset


def test_page_response_accepts_realistic_values() -> None:
    response = PageResponse(
        items=[{"id": 1}, {"id": 2}],
        total=42,
        page=3,
        page_size=10,
        total_pages=5,
    )

    assert response.items == [{"id": 1}, {"id": 2}]
    assert response.total == 42
    assert response.page == 3
    assert response.page_size == 10
    assert response.total_pages == 5


def test_page_response_constructs_with_default_like_values() -> None:
    response = PageResponse(
        items=[],
        total=0,
        page=1,
        page_size=20,
        total_pages=1,
    )

    assert response.items == []
    assert response.total == 0
    assert response.page == 1
    assert response.page_size == 20
    assert response.total_pages == 1
