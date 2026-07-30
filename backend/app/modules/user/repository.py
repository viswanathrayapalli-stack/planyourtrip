from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.user.models import User
from app.shared.repositories import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self):
        super().__init__(User)

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.scalar(stmt)


user_repository = UserRepository()