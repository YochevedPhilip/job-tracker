from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

from enum import Enum as PyEnum


class StatusEnum(PyEnum):
    CV_SENT = "cv_sent"
    AWAITING_RESPONSE = "awaiting_response"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    REJECTED = "rejected"
    OFFER_RECEIVED = "offer_received"
    WITHDRAWN = "withdrawn"

class ProccesModel(Base):
    __tablename__ = 'procceses'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    status = Column(SqlEnum(StatusEnum), default = StatusEnum.CV_SENT)

    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("UserModel", back_populates="procceses")

    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship("CompanyModel", back_populates="procceses")