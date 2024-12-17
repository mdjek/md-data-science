from confluent_kafka import Producer, Consumer, KafkaError
import json
from entities import Order
from init_pg_db import db_context
from constants import KAFKA_BOOTSTRAP_SERVERS, KAFKA_ORDER_TOPIC
from utils import connect_redis, insert_data_into_redis
import threading

# Redis client
redis_client = connect_redis()

conf = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,  # Адрес Kafka брокера
    "group.id": KAFKA_ORDER_TOPIC,  # ID группы заказов
    "auto.offset.reset": "earliest",  # Начинать с самого раннего сообщения
}


# Kafka Producer
def get_kafka_producer():
    return Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})


# Kafka Consumer
def kafka_consumer_service():
    consumer = Consumer(**conf)
    consumer.subscribe([KAFKA_ORDER_TOPIC])

    while True:
        msg = consumer.poll(1.0)  # Ожидание сообщения в течение 1 секунды

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Ошибка Kafka: {msg.error()}")
                break

        # Обработка сообщения
        order_data = json.loads(msg.value().decode("utf-8"))

        with db_context() as db:
            try:
                # put
                if order_data.get("id"):
                    existing_order = (
                        db.query(Order)
                        .filter(Order.id == order_data.get("id"))
                        .first()
                    )

                    name = order_data.get("name")
                    description = order_data.get("description")
                    user_id = order_data.get("user_id")

                    existing_order.name = (
                        name if isinstance(name, str) else existing_order.name
                    )
                    existing_order.description = (
                        description
                        if isinstance(description, str)
                        else existing_order.description
                    )
                    existing_order.user_id = (
                        user_id
                        if isinstance(user_id, int)
                        else existing_order.user_id
                    )

                    db.commit()
                    db.refresh(existing_order)

                    data = db.query(Order).all()

                    if data:
                        insert_data_into_redis(
                            data, "orders", ["id", "user_id"]
                        )

                # post
                else:
                    db_order = Order(**order_data)

                    db.add(db_order)
                    db.commit()
                    db.refresh(db_order)

                    data = db.query(Order).all()

                    if data:
                        insert_data_into_redis(
                            data, "orders", ["id", "user_id"]
                        )
            except Exception as e:
                print(f"Processing kafka message error: {e}")
                return None

    consumer.close()


# Запуск Kafka Consumer в фоне
def run_kafka_consumer():
    thread = threading.Thread(target=kafka_consumer_service, daemon=True)
    thread.start()
