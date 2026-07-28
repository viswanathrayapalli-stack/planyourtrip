from fastapi import Depends
from sqlalchemy.orm import Session

from app.modules.destination.repository import DestinationRepository
from app.modules.destination.service import DestinationService
from app.shared.database.session import get_db


def get_destination_service(
    db: Session = Depends(get_db),
) -> DestinationService:
    repository = DestinationRepository(db)
    return DestinationService(repository)