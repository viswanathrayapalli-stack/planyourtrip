from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_attachment_service,
    get_current_user,
    get_db,
)
from app.modules.attachment.schemas import (
    AttachmentCreate,
    AttachmentResponse,
)
from app.modules.attachment.service import AttachmentService
from app.modules.user.models import User
from app.shared.pagination import PageResponse, PaginationParams

router = APIRouter(prefix="/attachments", tags=["Attachments"])


@router.get(
    "/trips/{trip_id}",
    response_model=PageResponse[AttachmentResponse],
)
def get_attachments(
    trip_id: int,
    db: Session = Depends(get_db),
    service: AttachmentService = Depends(get_attachment_service),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
):
    return service.get_by_trip_id_paginated(
        db=db,
        trip_id=trip_id,
        user_id=current_user.id,
        pagination=pagination,
    )


@router.post(
    "/",
    response_model=AttachmentResponse,
)
def create_attachment(
    trip_id: Annotated[int, Form(...)],
    category: Annotated[str, Form(...)],
    file: Annotated[UploadFile, File(...)],
    db: Session = Depends(get_db),
    service: AttachmentService = Depends(get_attachment_service),
    current_user: User = Depends(get_current_user),
):
    request = AttachmentCreate(
        trip_id=trip_id,
        category=category,
        file=file,
    )

    return service.create(
        db=db,
        request=request,
        user_id=current_user.id,
    )


@router.delete(
    "/{attachment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    service: AttachmentService = Depends(get_attachment_service),
    current_user: User = Depends(get_current_user),
):
    service.delete(
        db=db,
        attachment_id=attachment_id,
        user_id=current_user.id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
