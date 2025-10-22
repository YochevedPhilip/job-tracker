from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import update, select, delete
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session:Session, model:Type[ModelType]):
        self.session = session
        self.model = model

    def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Optional[ModelType]:
       stmt = select(self.model).where(self.model.id == id)
       result = self.session.execute(stmt)
       return result.scalar_one_or_none()

    def get_all(self) -> List[ModelType]:
        stmt = select(self.model)
        result = self.session.execute(stmt)
        return result.scalars().all()

    def update(self, id: int, **fields) -> ModelType:
        stmt = update(self.model).where(self.model.id == id).values(**fields)
        self.session.execute(stmt)
        self.session.commit()
        self.session.refresh(self.get_by_id(id))
        return self.get_by_id(id)



    def delete(self, id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        result = self.session.execute(stmt)
        self.session.commit()
        return result.rowcount>0




