from fastapi import APIRouter, Depends
from app.core.dependencies import get_destination_service

from app.modules.destination.schemas import (
    DestinationCreate,
    DestinationResponse,
    DestinationUpdate,
)
from app.modules.destination.service import DestinationService
from app.modules.place.schemas import PlaceResponse
from app.shared.schemas import MessageResponse

from sqlalchemy.orm import Session
from app.shared.database.session import get_db

#from app.shared.utils.response import success_response

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("", response_model=list[DestinationResponse])   
def get_destinations(
    db: Session = Depends(get_db),
    service: DestinationService = Depends(get_destination_service),
):
    return service.get_all(db)  
    


@router.post("", response_model=DestinationResponse)
def create_destination(
    request: DestinationCreate,
    db: Session = Depends(get_db),
    service: DestinationService = Depends(get_destination_service),
):
    return service.create(db,request)

@router.get("/{destination_id}", response_model=DestinationResponse)
def get_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    service: DestinationService = Depends(get_destination_service),
):
    return service.get_by_id(db,destination_id)


@router.get(
    "/{destination_id}/places",
    response_model=list[PlaceResponse],
)
def get_destination_places(
    destination_id: int,
    db: Session = Depends(get_db),
    service: DestinationService = Depends(get_destination_service),
):
    return service.get_places(db, destination_id)

@router.put("/{destination_id}", response_model=DestinationResponse)
def update_destination(
    destination_id: int,
    request: DestinationUpdate,
    db: Session = Depends(get_db),
    service: DestinationService = Depends(get_destination_service),
):
    return service.update(db, destination_id, request)


@router.delete(
    "/{destination_id}",
    response_model=MessageResponse,
)
def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    service: DestinationService = Depends(get_destination_service),
):
    service.delete(db, destination_id)

    return MessageResponse(
        success=True,
        message="Destination deleted successfully.",
    )
