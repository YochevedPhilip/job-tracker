from sqlalchemy.orm import Session

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse


class UserService:
    def __init__(self, db:Session):
        self.repo = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> UserResponse:
        if self.repo.get_by_email(user_in.email):
            raise ValueError("User with this email already exists")
        user_model = User(**user_in.model_dump())
        new_user = self.repo.create(user_model)
        return UserResponse.model_validate(new_user)





