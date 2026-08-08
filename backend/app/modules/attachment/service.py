from sqlalchemy.orm import Session

from app.modules.attachment.repository import AttachmentRepository
from app.modules.attachment.schemas import AttachmentCreate, AttachmentResponse
from app.shared.authorization import AuthorizationService
from app.modules.trip.constants import TRIP_NOT_FOUND
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException
from app.shared.pagination import PageResponse, PaginationParams
from app.shared.storage.file_validator import FileValidator
from app.shared.storage.local_storage import LocalStorageService


class AttachmentService:

    def __init__(
        self,
        repository: AttachmentRepository,
        trip_repository: TripRepository,
        authorization_service: AuthorizationService,
        storage: LocalStorageService,
        file_validator: FileValidator,
    ):
        self.repository = repository
        self.trip_repository = trip_repository
        self.authorization_service = authorization_service
        self.storage = storage
        self.file_validator = file_validator

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
    ) -> list[AttachmentResponse]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        attachments = self.repository.get_by_trip_id(db, trip_id)

        response: list[AttachmentResponse] = []

        for attachment in attachments:
            response.append(
                AttachmentResponse(
                    id=attachment.id,
                    trip_id=attachment.trip_id,
                    file_name=attachment.file_name,
                    original_file_name=attachment.original_file_name,
                    file_type=attachment.file_type,
                    file_size=attachment.file_size,
                    file_path=attachment.file_path,
                    category=attachment.category,
                    created_at=attachment.created_at,
                )
            )

        return response

    def get_by_trip_id_paginated(
        self,
        db: Session,
        trip_id: int,
        user_id: int,
        pagination: PaginationParams,
    ) -> PageResponse[AttachmentResponse]:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=trip_id,
            current_user_id=user_id,
        )

        page = self.repository.get_by_trip_id_paginated(
            db=db,
            trip_id=trip_id,
            pagination=pagination,
        )

        return PageResponse(
            items=[
                AttachmentResponse.model_validate(item)
                for item in page.items
            ],
            total=page.total,
            page=page.page,
            page_size=page.page_size,
            total_pages=page.total_pages,
        )

    def create(
        self,
        db: Session,
        request: AttachmentCreate,
        user_id: int,
    ) -> AttachmentResponse:
        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=request.trip_id,
            current_user_id=user_id,
        )

        file = request.file

        self.file_validator.validate(file)
        generated_filename, file_path = self.storage.save_file(file)

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        attachment = self.repository.model(
            trip_id=request.trip_id,
            file_name=generated_filename,
            original_file_name=file.filename or "",
            file_type=file.content_type or "",
            file_size=file_size,
            file_path=file_path,
            category=request.category,
        )
        attachment = self.repository.create(db, attachment)

        return AttachmentResponse(
            id=attachment.id,
            trip_id=attachment.trip_id,
            file_name=attachment.file_name,
            original_file_name=attachment.original_file_name,
            file_type=attachment.file_type,
            file_size=attachment.file_size,
            file_path=attachment.file_path,
            category=attachment.category,
            created_at=attachment.created_at,
        )

    def delete(
        self,
        db: Session,
        attachment_id: int,
        user_id: int,
    ) -> None:
        attachment = self.repository.get_by_id(db, attachment_id)

        if attachment is None:
            raise ResourceNotFoundException("Attachment not found.")

        self.authorization_service.ensure_trip_owner(
            db=db,
            trip_id=attachment.trip_id,
            current_user_id=user_id,
        )

        self.repository.delete(db, attachment)
