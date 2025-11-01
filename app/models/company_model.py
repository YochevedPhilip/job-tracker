from sqlalchemy import Integer, String, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index = True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="companies")

    processes = relationship("Process", back_populates="company")
