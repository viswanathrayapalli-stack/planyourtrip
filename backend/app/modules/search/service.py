from sqlalchemy.orm import Session

from app.modules.search.repository import TripSearchRepository
from app.modules.trip.models import Trip


class TripSearchService:

    def __init__(self, repository: TripSearchRepository):
        self.repository = repository

    def search_by_title(
        self,
        db: Session,
        keyword: str,
    ) -> list[Trip]:
        keyword = keyword.strip()

        if keyword == "":
            return []

        return self.repository.search_by_title(db, keyword)
