import json
from init_db import SessionLocal
from entities import User, Order, Task
from typing import Callable

def load_user(entity):
    return User(
        username=entity["username"],
        first_name=entity["first_name"],
        last_name=entity["last_name"],
        email=entity["email"]
    )

def load_order(entity):
    return Order(
        name=entity["name"],
        description=entity["description"],
        user_id=entity["user_id"],
    )

def load_task(entity):
    return Task(
        name=entity["name"],
        description=entity["description"],
        order_id=entity["order_id"],
    )

callbacks = {
    "users": load_user,
    "tasks": load_task,
    "orders": load_order
}

def load_table_mocks(data: list, callback: Callable):
    db = SessionLocal()

    for entity in data:
        entityDB = callback(entity)

        db.add(entityDB)
        db.commit()

def load_json_mock():
    json_list = ("users","tasks", "orders")

    for table_name in json_list:
        f_opened = open(f"./mock-data/{table_name}.json")
        data = json.load(f_opened)

        load_table_mocks(data, callbacks[table_name])
        f_opened.close()