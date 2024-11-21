from fastapi import APIRouter, Depends, HTTPException
from typing import List

from routers.auth import get_current_client
from entities import ResponseUserEntity, CreateUserEntity, User
from init_pg_db import get_db
from sqlalchemy.orm import Session
from pymongo import MongoClient

# Настройка Mongo
MONGODB_URI = "mongodb://root:rootpasswd@mongo:27017/"   
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=1000)
db = client['mongo_profi_db']
collection = db['users']

router = APIRouter()

# GET /users - Получить список пользователей (требует аутентификации)
# @router.get("/users", response_model=List[ResponseUserEntity], tags=["Users"], dependencies=[Depends(get_current_client)])
@router.get("/users", response_model=List[ResponseUserEntity], tags=["Users"])
def get_users():
    result = list(collection.find())

    for user in result:
        user["id"] = str(user["_id"])

    return result

# POST /users - Создать нового пользователя (требует аутентификации)
@router.post("/users", response_model=ResponseUserEntity, tags=["Users"], dependencies=[Depends(get_current_client)])
# @router.post("/users", response_model=ResponseUserEntity, tags=["Users"])
def create_user(new_user: CreateUserEntity, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == new_user.username).first():
        raise HTTPException(status_code=404, detail="User with such username already exist")
    
    if db.query(User).filter(User.email == new_user.email).first():
        raise HTTPException(status_code=404, detail="User with such email already exist")

    db_user = User(**new_user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# GET /users/{username} - Поиск пользователя по username (требует аутентификации)
@router.get("/users/{username}", response_model=ResponseUserEntity, tags=["Users"], dependencies=[Depends(get_current_client)])
# @router.get("/users/{username}", response_model=ResponseUserEntity, tags=["Users"])
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    
    if user.id:
        return user
    raise HTTPException(status_code=404, detail="User with such username does not exist") 
    
