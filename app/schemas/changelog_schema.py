from pydantic import BaseModel
from datetime import datetime
from app.models.process_model import StatusEnum


class ChangelogResponse(BaseModel):
    changed_to : StatusEnum
    changed_at : datetime

    class Config:
        orm_mode = True