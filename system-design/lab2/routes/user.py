from fastapi import APIRouter, Depends, Form, HTTPException
from datetime import timedelta, datetime
from typing import Dict, Optional, List

from routes.auth import get_current_client
from entities import UserEntity


router = APIRouter()

# Временное хранилище для пользователей
users_db = []

# GET /users - Получить всех пользователей (требует аутентификации)
@router.get("/users", response_model=List[UserEntity])
def get_users(current_user: str = Depends(get_current_client)):
    return users_db