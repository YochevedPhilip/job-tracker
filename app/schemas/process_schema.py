
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Text
from app.models.process_model import StatusEnum

class ProcessBase(BaseModel):
    job_number: str
    company_id: str

class ProcessCreate(ProcessBase):
    user_id: int
    status: StatusEnum | None = None
    created_at: datetime | None = None
    description: Text | None = None

class ProcessUpdate(ProcessBase):
        user_id: int
        status: StatusEnum | None = None
        description: Text | None = None



class ProcessResponse(ProcessBase):
    status: StatusEnum
    created_at: datetime
    updated_at: datetime
    description: Text

    class Config:
        orm_mode = True
