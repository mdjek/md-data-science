import json
from init_db import SessionLocal
from entities import User, Order, Task
from typing import Callable

def load_user(entity):
    return User(
        username=entity["username"],
        first_name=entity["first_name"],
        last_name=entity["last_name"],
        email=entity["email"],
        password=entity["password"]
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


def load_table_mock(data: list, callback: Callable):
    db = SessionLocal()

    for entity in data:
        entityDB = callback(entity)

        db.add(entityDB)
        db.commit()

    db.close()

def load_mock_data():
    tableToCallback = {
        "users": load_user,
        "tasks": load_task,
        "orders": load_order
    }

    for table_name in tableToCallback.keys():
        f_opened = open(f"./mocks/{table_name}.json")
        data = json.load(f_opened)

        load_table_mock(data, tableToCallback[table_name])
        f_opened.close()