from fastapi import APIRouter, Depends, HTTPException
from typing import List

from routers.auth import get_current_client
from entities import ResponseOrderEntity, CreateOrderEntity, Order
from init_pg_db import get_db
from sqlalchemy.orm import Session
from utils import insert_data_into_redis, get_data_from_redis
from confluent_kafka import Producer
from services.kafka import get_kafka_producer, run_kafka_consumer
from constants import KAFKA_ORDER_TOPIC
import json
import uuid

run_kafka_consumer()
router = APIRouter()


# GET /orders - Получить список заказов (требует аутентификации)
@router.get(
    "/orders",
    response_model=List[ResponseOrderEntity],
    tags=["Orders"],
    dependencies=[Depends(get_current_client)],
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
@router.post(
    "/orders",
    response_model=CreateOrderEntity,
    tags=["Orders"],
    dependencies=[Depends(get_current_client)],
)
# @router.post("/orders", response_model=ResponseOrderEntity, tags=["Orders"])
def create_order(
    new_order: CreateOrderEntity,
    db: Session = Depends(get_db),
    producer: Producer = Depends(get_kafka_producer),
):
    producer.produce(
        KAFKA_ORDER_TOPIC,
        key=str(f"{uuid.uuid4()}_{new_order.name}"),
        value=json.dumps(new_order.dict()).encode("utf-8"),
    )
    producer.flush()

    return new_order


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
    producer.produce(
        KAFKA_ORDER_TOPIC,
        key=str(order_id),
        value=json.dumps({**updated_order.dict(), "id": order_id}).encode(
            "utf-8"
        ),
    )
    producer.flush()

    return {**updated_order.dict(), "id": order_id}


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
