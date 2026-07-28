from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.destination.repository import DestinationRepository

from app.modules.destination.schemas import (
    DestinationCreate,
    DestinationResponse,
    DestinationUpdate,
)

from app.modules.destination.service import DestinationService
from app.shared.database.session import get_db

router = APIRouter(prefix="/destinations", tags=["Destinations"])


def get_service(db: Session = Depends(get_db)) -> DestinationService:
    repository = DestinationRepository(db)
    return DestinationService(repository)


@router.get("", response_model=list[DestinationResponse])
def get_destinations(
    service: DestinationService = Depends(get_service),
):
    return service.get_all()


@router.post("", response_model=DestinationResponse)
def create_destination(
    request: DestinationCreate,
    service: DestinationService = Depends(get_service),
):
    return service.create(request)

@router.get("/{destination_id}", response_model=DestinationResponse)
def get_destination(
    destination_id: int,
    service: DestinationService = Depends(get_service),
):
    return service.get_by_id(destination_id)

@router.put("/{destination_id}", response_model=DestinationResponse)
def update_destination(
    destination_id: int,
    request: DestinationUpdate,
    service: DestinationService = Depends(get_service),
):
    return service.update(destination_id, request)

@router.delete("/{destination_id}")
def delete_destination(
    destination_id: int,
    service: DestinationService = Depends(get_service),
):
    service.delete(destination_id)
    return {
        "success": True,
        "message": "Destination deleted successfully.",
    }

