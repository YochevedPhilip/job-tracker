
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED
    )
def create_user(
        user_in : UserCreate,
        db : Session = Depends(get_db)
):
    serv = UserService(db)
    try:
        user = serv.create_user(user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )


@router.get(
    "/",
    response_model= List[UserResponse]
)
def read_users(
        db : Session = Depends(get_db)
):
    repo = UserRepository(db)
    users = repo.get_all()
    return users

@router.get(
    "/{user_id}",
    response_model = UserResponse
)
def read_user(
        user_id : int,
        db : Session = Depends(get_db)
):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code = 404, detail="User not found")
    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id : int,
    user_update : UserUpdate,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = repo.update(user.id, password=user_update.password)
    return updated_user

@router.delete(
"/{user_id}",
status_code=status.HTTP_204_NO_CONTENT
)

def delete_user(
    user_id : int,
    db : Session = Depends(get_db)
):
    repo = UserRepository(db)
    succes = repo.delete(user_id)
    if not succes:
        raise HTTPException(status_code = 404, detail="User not found")
    return None





