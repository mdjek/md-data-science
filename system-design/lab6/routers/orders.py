from fastapi import APIRouter, Depends, HTTPException
from typing import List
from routers.auth import get_current_client
from entities import ResponseOrderEntity, CreateOrderEntity, Order
from init_pg_db import get_db
from sqlalchemy.orm import Session
from utils import insert_data_into_redis, get_data_from_redis
from confluent_kafka import Producer
# from services.kafka import get_kafka_producer, kafka_consumer_service

router = APIRouter()


# GET /orders - Получить список заказов (требует аутентификации)
@router.get(
    "/orders", response_model=List[ResponseOrderEntity], tags=["Orders"], dependencies=[Depends(get_current_client)]
)
# @router.get("/orders", response_model=List[ResponseOrderEntity], tags=["Orders"])
def get_orders(db: Session = Depends(get_db)):
    cached_data = get_data_from_redis("orders:*")

    if cached_data:
        return cached_data
    else:
        data = db.query(Order).all()

        if data:
            insert_data_into_redis(data, "orders", ["id", "user_id"])
            return data

        raise HTTPException(status_code=404, detail="Orders not found")


# POST /orders - Создать заказ (требует аутентификации)
@router.post("/orders", response_model=ResponseOrderEntity, tags=["Orders"], dependencies=[Depends(get_current_client)])
# @router.post("/orders", response_model=ResponseOrderEntity, tags=["Orders"])
def create_order(
    new_order: CreateOrderEntity, db: Session = Depends(get_db), producer: Producer = Depends(get_kafka_producer)
):
    db_order = Order(**new_order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    data = db.query(Order).all()

    if data:
        insert_data_into_redis(data, "orders", ["id", "user_id"])

    return db_order


# PUT /orders/{order_id} - Редактировать существующий заказ (требует аутентификации)
@router.put(
    "/orders/{order_id}",
    response_model=ResponseOrderEntity,
    tags=["Orders"],
    dependencies=[Depends(get_current_client)],
)
# @router.put("/orders/{order_id}", response_model=ResponseOrderEntity, tags=["Orders"])
def edit_order(
    order_id: int,
    updated_order: CreateOrderEntity,
    db: Session = Depends(get_db),
    producer: Producer = Depends(get_kafka_producer),
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order:
        order.name = updated_order.name if isinstance(updated_order.name, str) else order.name
        order.description = (
            updated_order.description if isinstance(updated_order.description, str) else order.description
        )
        order.user_id = updated_order.user_id if isinstance(updated_order.user_id, int) else order.user_id

        db.commit()
        db.refresh(order)

        data = db.query(Order).all()

        if data:
            insert_data_into_redis(data, "orders", ["id", "user_id"])

        return order

    raise HTTPException(status_code=404, detail="Order not found")


# GET /orders/user/{user_id} - Получить всех заказы для пользователя (требует аутентификации)
@router.get(
    "/orders/user/{user_id}",
    response_model=List[ResponseOrderEntity],
    tags=["Orders"],
    dependencies=[Depends(get_current_client)],
)
# @router.get("/orders/user/{user_id}", response_model=List[ResponseOrderEntity], tags=["Orders"])
def get_orders_for_user(user_id: int, db: Session = Depends(get_db)):
    cached_data = get_data_from_redis(f"orders:*:{user_id}")

    if cached_data:
        return cached_data
    else:
        data = db.query(Order).all()

        if data:
            insert_data_into_redis(data, "orders", ["id", "user_id"])
            return data

        raise HTTPException(status_code=404, detail="Orders not found")
