from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class PageResponse(GenericModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
