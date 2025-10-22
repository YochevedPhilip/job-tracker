from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models import Company

class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session:Session):
        super().__init__(session, Company)
