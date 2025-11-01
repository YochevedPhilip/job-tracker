
from sqlalchemy.orm import Session

from app.models import Company
from app.repositories.company_repository import CompanyRepository




class CompanyService:
    def __init__(self, db:Session):
        self.repo = CompanyRepository(db)

    def get_or_create(self, company_in:Company):
        company = self.repo.get_by_name_and_user(company_in.name, company_in.user_id)
        if company:
            return company
        return self.repo.create(company_in)