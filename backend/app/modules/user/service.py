from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate, UserUpdate
from app.shared.exceptions.exceptions import (
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)


class UserService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    def get_all(
        self,
        db: Session,
    ) -> list[User]:
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> User:

        user = self.repository.get_by_id(db, user_id)

        if user is None:
            raise ResourceNotFoundException("User not found.")

        return user

    def create(
        self,
        db: Session,
        request: UserCreate,
    ) -> User:

        existing_user = self.repository.get_by_email(
            db,
            request.email,
        )

        if existing_user:
            raise ResourceAlreadyExistsException(
                "Email is already registered."
            )

        hashed_password = hash_password(request.password)

        user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=hashed_password,
            is_active=True,
        )

        return self.repository.create(db, user)

    def update(
        self,
        db: Session,
        user_id: int,
        request: UserUpdate,
    ) -> User:

        user = self.get_by_id(db, user_id)

        update_data = request.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = hash_password(
                update_data.pop("password")
            )

        for key, value in update_data.items():
            setattr(user, key, value)

        return self.repository.update(db, user)

    def delete(
        self,
        db: Session,
        user_id: int,
    ) -> None:

        user = self.get_by_id(db, user_id)

        self.repository.delete(db, user)