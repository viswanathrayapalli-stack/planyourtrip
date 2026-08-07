from sqlalchemy.orm import Session

from app.modules.attachment.repository import AttachmentRepository
from app.modules.attachment.schemas import AttachmentCreate, AttachmentResponse
from app.modules.trip.constants import TRIP_NOT_FOUND
from app.modules.trip.repository import TripRepository
from app.shared.exceptions.exceptions import ResourceNotFoundException


class AttachmentService:

    def __init__(
        self,
        repository: AttachmentRepository,
        trip_repository: TripRepository,
    ):
        self.repository = repository
        self.trip_repository = trip_repository

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[AttachmentResponse]:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException(TRIP_NOT_FOUND)

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

    def create(
        self,
        db: Session,
        request: AttachmentCreate,
    ) -> AttachmentResponse:
        trip = self.trip_repository.get_by_id(db, request.trip_id)

        if trip is None:
            raise ResourceNotFoundException(TRIP_NOT_FOUND)

        attachment = self.repository.model(**request.model_dump())
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
    ) -> None:
        attachment = self.repository.get_by_id(db, attachment_id)

        if attachment is None:
            raise ResourceNotFoundException("Attachment not found.")

        self.repository.delete(db, attachment)
