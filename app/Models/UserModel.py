from sqlalchemy import Column, Integer, String, Boolean, DateTime, column
from sqlalchemy.sql import func
from app.database import Base

class UserModel(Base):
    __tablename__ = 'users'
    id = column(Integer, primary_key=True, index=True)