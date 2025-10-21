from sqlalchemy import Integer, DateTime, Column, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.process_model import StatusEnum
from app.database import Base

class ChangelogModel(Base):
    __tablename__ = 'changelog'
    id = Column(Integer, primary_key=True)
    changed_to = Column(SqlEnum(StatusEnum), nullable=False)
    changed_at = Column(DateTime(timezone=True), default=func.now())

    process_id = Column(Integer, ForeignKey('processes.id'))

    owner = relationship("ProcessModel", back_populates="changes")
