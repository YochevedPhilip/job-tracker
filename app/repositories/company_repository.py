from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models import Company


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session:Session):
        super().__init__(session, Company)

    def get_by_user(self, user_id: int) -> List[Company]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = self.session.execute(stmt)
        return result.scalars().all()

    def get_by_name_and_user(self, name: str, user_id: int) -> Company:
        stmt = select(self.model).where(self.model.name == name, self.model.user_id == user_id)
        result = self.session.execute(stmt)
        return result.scalars().first()







