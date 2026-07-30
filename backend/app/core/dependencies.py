from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.modules.destination.repository import DestinationRepository
from app.modules.destination.service import DestinationService
from app.modules.identity.constants import UNAUTHORIZED
from app.modules.trip.repository import TripRepository
from app.modules.trip.service import TripService
from app.modules.user.models import User
from app.modules.user.repository import UserRepository, user_repository
from app.modules.user.service import UserService
from app.shared.database.session import get_db
from app.shared.exceptions.exceptions import AuthenticationException


def get_destination_service(
    db: Session = Depends(get_db),
):
    repository = DestinationRepository()
    return DestinationService(repository)


def get_trip_service(
    db: Session = Depends(get_db),
):
    repository = TripRepository()
    return TripService(repository)


def get_user_service(
    db: Session = Depends(get_db),
):
    repository = UserRepository()
    return UserService(repository)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/identity/login"
)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationException(UNAUTHORIZED)

    except JWTError as exc:
        raise AuthenticationException(UNAUTHORIZED) from exc

    user = user_repository.get_by_id(
        db=db,
        entity_id=int(user_id),
    )

    if user is None:
        raise AuthenticationException(UNAUTHORIZED)

    if not user.is_active:
        raise AuthenticationException(UNAUTHORIZED)

    return user