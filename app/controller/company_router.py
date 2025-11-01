from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.repositories.company_repository import CompanyRepository
from app.schemas.company_schema import CompanyCreate, CompanyResponse

router = APIRouter(
    prefix = "/companies",
    tags = ["companies"]
)

@router.get(
    "/{user_id}",
    response_model=List[CompanyResponse]
)
def read_companies_by_user(
        user_id : int,
        db : Session = Depends(get_db)
):
    repo = CompanyRepository(db)
    companies = repo.get_by_user(user_id)
    return companies

