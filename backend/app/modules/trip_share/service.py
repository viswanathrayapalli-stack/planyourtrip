from sqlalchemy.orm import Session

from app.modules.trip.constants import TRIP_NOT_FOUND
from app.modules.trip.repository import TripRepository
from app.modules.trip_share.repository import TripShareRepository
from app.modules.trip_share.schemas import TripShareCreate, TripShareResponse
from app.modules.user.repository import UserRepository
from app.shared.email import EmailService
from app.shared.exceptions.exceptions import ResourceNotFoundException, ValidationException


class TripShareService:

    def __init__(
        self,
        repository: TripShareRepository,
        trip_repository: TripRepository,
        user_repository: UserRepository,
        email_service: EmailService,
    ):
        self.repository = repository
        self.trip_repository = trip_repository
        self.user_repository = user_repository
        self.email_service = email_service

    def get_by_trip_id(
        self,
        db: Session,
        trip_id: int,
    ) -> list[TripShareResponse]:
        trip = self.trip_repository.get_by_id(db, trip_id)

        if trip is None:
            raise ResourceNotFoundException(TRIP_NOT_FOUND)

        shares = self.repository.get_by_trip_id(db, trip_id)

        response: list[TripShareResponse] = []

        for share in shares:
            user = self.user_repository.get_by_id(db, share.user_id)

            if user is None:
                raise ResourceNotFoundException("User not found.")

            response.append(
                TripShareResponse(
                    id=share.id,
                    trip_id=share.trip_id,
                    user_id=share.user_id,
                    user_name=user.full_name,
                    user_email=user.email,
                    permission=share.permission,
                    created_at=share.created_at,
                )
            )

        return response

    def create(
        self,
        db: Session,
        request: TripShareCreate,
    ) -> TripShareResponse:
        trip = self.trip_repository.get_by_id(db, request.trip_id)

        if trip is None:
            raise ResourceNotFoundException(TRIP_NOT_FOUND)

        user = self.user_repository.get_by_id(db, request.user_id)

        if user is None:
            raise ResourceNotFoundException("User not found.")

        existing_share = self.repository.get_by_trip_and_user(
            db,
            request.trip_id,
            request.user_id,
        )

        if existing_share is not None:
            raise ValidationException("Trip is already shared with this user.")

        share = self.repository.model(**request.model_dump())
        share = self.repository.create(db, share)

        try:
            self.email_service.send_email(
                to_email=user.email,
                subject="Trip Invitation",
                body=(
                    f"Hello {user.full_name},\n\n"
                    f"You have been invited to join trip #{share.trip_id}.\n"
                    f"Permission: {share.permission}."
                ),
            )
        except Exception:
            pass

        return TripShareResponse(
            id=share.id,
            trip_id=share.trip_id,
            user_id=share.user_id,
            user_name=user.full_name,
            user_email=user.email,
            permission=share.permission,
            created_at=share.created_at,
        )

    def delete(
        self,
        db: Session,
        share_id: int,
    ) -> None:
        share = self.repository.get_by_id(db, share_id)

        if share is None:
            raise ResourceNotFoundException("Trip share not found.")

        self.repository.delete(db, share)
