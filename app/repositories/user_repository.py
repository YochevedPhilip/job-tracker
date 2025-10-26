from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models import User
from app.schemas.user_schema import UserResponse


class UserRepository(BaseRepository[User]):
    def __init__(self, session:Session):
        super().__init__(session, User)

    def get_by_email(self, email:EmailStr) -> UserResponse:
        stmt = select(self.model).where(self.model.email == email)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


