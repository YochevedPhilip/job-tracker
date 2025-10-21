from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    user_id: int

class CompanyResponse(CompanyBase):
    id: int

    class Config:
        orm_mode = True
