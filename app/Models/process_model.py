from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Enum as SqlEnum, Text
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

class ProcessModel(Base):
    __tablename__ = 'processes'
    id = Column(Integer, primary_key=True)
    job_number = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    status = Column(SqlEnum(StatusEnum), default = StatusEnum.CV_SENT)
    description = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("UserModel", back_populates="processes")

    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship("CompanyModel", back_populates="processes")

    changes = relationship("ChangelogModel", back_populates="owner")