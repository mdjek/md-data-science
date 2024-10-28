from fastapi import APIRouter, Depends, Form, HTTPException
from datetime import timedelta, datetime
from typing import Dict, Optional, List

from routers.auth import get_current_client
from entities import UserEntity


router = APIRouter()

# Временное хранилище для пользователей
users_db = []

# GET /users - Получить список пользователей (требует аутентификации)
@router.get("/users", response_model=List[UserEntity])
def get_users(current_user: str = Depends(get_current_client)):
    return users_db

# POST /users - Создать нового пользователя (требует аутентификации)
@router.post("/users", response_model=UserEntity)
def create_user(newUser: UserEntity, current_user: str = Depends(get_current_client)):
    for user in users_db:
        if user.id == newUser.id:
            raise HTTPException(status_code=404, detail="User already exist")
        if user.username == newUser.username:
            raise HTTPException(status_code=404, detail="User with such username already exist")
    users_db.append(newUser)
    return newUser

# GET /users/{username} - Поиск пользователя по username (требует аутентификации)
@router.get("/users/{username}", response_model=UserEntity)
def get_user(username: str, current_user: str = Depends(get_current_client)):
    for user in users_db:
        if user.username == username:
            return user
        raise HTTPException(status_code=404, detail="User with such username does not exist") 
