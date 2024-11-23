from fastapi import APIRouter, Depends, HTTPException
from typing import List

from routers.auth import get_current_client
from entities import ResponseUserEntity, CreateUserEntity, User
from init_pg_db import get_db
from sqlalchemy.orm import Session
from pymongo import MongoClient
from constants import MONGODB_URI

# Настройка Mongo  
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
    query_by_user_name = { "username": new_user.username }
    query_by_email = { "email": new_user.email }
    
    user_with_username = collection.find_one(query_by_user_name)
    user_with_email = collection.find_one(query_by_email)

    if user_with_username:
        raise HTTPException(status_code=404, detail="User with such username already exist")
    
    if user_with_email:
        raise HTTPException(status_code=404, detail="User with such email already exist")

    insert_user = new_user.dict()
    # insert_user["password"] = pwd_context.hash(insert_user["password"])
    user_id = collection.insert_one(insert_user).inserted_id    
    insert_user["id"] = str(user_id)

    return insert_user

# GET /users/{username} - Поиск пользователя по username (требует аутентификации)
@router.get("/users/{username}", response_model=ResponseUserEntity, tags=["Users"], dependencies=[Depends(get_current_client)])
# @router.get("/users/{username}", response_model=ResponseUserEntity, tags=["Users"])
def get_user(username: str, db: Session = Depends(get_db)):
    query = { "username": username }
    user = collection.find_one(query)

    if user:
        user["id"] = str(user["_id"])
        return user
    else:
        raise HTTPException(status_code=404, detail="User with such username does not exist")

    
