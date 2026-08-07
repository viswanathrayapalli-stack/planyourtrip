from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_attachment_service, get_db
from app.modules.attachment.schemas import (
    AttachmentCreate,
    AttachmentResponse,
)
from app.modules.attachment.service import AttachmentService

router = APIRouter(prefix="/attachments", tags=["Attachments"])


@router.get(
    "/trips/{trip_id}",
    response_model=list[AttachmentResponse],
)
def get_attachments(
    trip_id: int,
    db: Session = Depends(get_db),
    service: AttachmentService = Depends(get_attachment_service),
):
    return service.get_by_trip_id(db, trip_id)


@router.post(
    "/",
    response_model=AttachmentResponse,
)
def create_attachment(
    request: AttachmentCreate,
    db: Session = Depends(get_db),
    service: AttachmentService = Depends(get_attachment_service),
):
    return service.create(db, request)


@router.delete(
    "/{attachment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    service: AttachmentService = Depends(get_attachment_service),
):
    service.delete(db, attachment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
