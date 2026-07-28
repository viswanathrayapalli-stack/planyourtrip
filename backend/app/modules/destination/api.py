from fastapi import APIRouter, Depends
from app.core.dependencies import get_destination_service

from app.modules.destination.schemas import (
    DestinationCreate,
    DestinationResponse,
    DestinationUpdate,
)
from app.modules.destination.service import DestinationService
from app.shared.schemas import MessageResponse

#from app.shared.utils.response import success_response

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("", response_model=list[DestinationResponse])
def get_destinations(
    service: DestinationService = Depends(get_destination_service),
):
    return service.get_all()
    


@router.post("", response_model=DestinationResponse)
def create_destination(
    request: DestinationCreate,
    service: DestinationService = Depends(get_destination_service),
):
    return service.create(request)

@router.get("/{destination_id}", response_model=DestinationResponse)
def get_destination(
    destination_id: int,
    service: DestinationService = Depends(get_destination_service),
):
    return service.get_by_id(destination_id)

@router.put("/{destination_id}", response_model=DestinationResponse)
def update_destination(
    destination_id: int,
    request: DestinationUpdate,
    service: DestinationService = Depends(get_destination_service),
):
    return service.update(destination_id, request)


@router.delete(
    "/{destination_id}",
    response_model=MessageResponse,
)
def delete_destination(
    destination_id: int,
    service: DestinationService = Depends(get_destination_service),
):
    service.delete(destination_id)

    return MessageResponse(
        success=True,
        message="Destination deleted successfully.",
    )
