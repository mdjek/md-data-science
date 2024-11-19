from fastapi import APIRouter, Depends, HTTPException
from typing import List

from routers.auth import get_current_client
from entities import ResponseOrderEntity

router = APIRouter()

# Временное хранилище для заказов
orders_db = []

# GET /orders - Получить список заказов (требует аутентификации)
@router.get("/orders", response_model=ResponseOrderEntity, dependencies=[Depends(get_current_client)])
def get_users():
    return orders_db

# POST /orders - Создать заказ (требует аутентификации)
@router.post("/orders", response_model=ResponseOrderEntity, dependencies=[Depends(get_current_client)])
def create_order(newOrder: ResponseOrderEntity):
    for order in orders_db:
        if order.id == newOrder.id:
            raise HTTPException(status_code=404, detail="Order already exist")
    orders_db.append(newOrder)
    return newOrder

# PUT /orders/{order_id} - Редактировать существующий заказ (требует аутентификации)
@router.put("/orders/{order_id}", response_model=ResponseOrderEntity, dependencies=[Depends(get_current_client)])
def create_task(order_id: int, updated_order: ResponseOrderEntity):
    for index, order in enumerate(orders_db):
        if order.id == order_id:
            orders_db[index] = updated_order
            return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

# GET /orders/user/{user_id} - Получить всех заказы для пользователя (требует аутентификации)
@router.get("/orders/user/{user_id}", response_model=ResponseOrderEntity, dependencies=[Depends(get_current_client)])
def get_orders_for_user(user_id: int):
    current_orders = []
    for order in orders_db:
        if order.user_id == user_id:
            current_orders.append(order)
    return current_orders