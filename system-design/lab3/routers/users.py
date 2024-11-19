from fastapi import APIRouter, Depends, HTTPException
from typing import List

from routers.auth import get_current_client
from entities import ResponseUserEntity, CreateUserEntity, User
from init_db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# GET /users - Получить список пользователей (требует аутентификации)
# @router.get("/users", response_model=ResponseUserEntity, dependencies=[Depends(get_current_client)])
@router.get("/users", response_model=List[ResponseUserEntity], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# POST /users - Создать нового пользователя (требует аутентификации)
# @router.post("/users", response_model=ResponseUserEntity, dependencies=[Depends(get_current_client)])
@router.post("/users", response_model=ResponseUserEntity, tags=["Users"])
def create_user(new_user: CreateUserEntity, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == new_user.username).first():
        raise HTTPException(status_code=404, detail="User with such username already exist")

    db_user = User(**new_user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# GET /users/{username} - Поиск пользователя по username (требует аутентификации)
# @router.get("/users/{username}", response_model=ResponseUserEntity, dependencies=[Depends(get_current_client)])
@router.get("/users/{username}", response_model=ResponseUserEntity, tags=["Users"])
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    
    if user.id:
        return user
    raise HTTPException(status_code=404, detail="User with such username does not exist") 
    
