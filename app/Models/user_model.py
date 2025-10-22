from sqlalchemy import  Integer, String, DateTime, Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index = True)
    password = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    companies = relationship("Company", back_populates="owner")
    processes = relationship("Process", back_populates="owner")
