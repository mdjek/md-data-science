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


def load_table_mock(data: list, loader: Callable):
    db = SessionLocal()

    for entity in data:
        entityDB = loader(entity)

        db.add(entityDB)
        db.commit()

    db.close()

def load_mock_data():
    mock_map = {
        "users": load_user,
        "tasks": load_task,
        "orders": load_order
    }

    for key in mock_map.keys():
        f_opened = open(f"./mocks/{key}.json")
        data = json.load(f_opened)

        load_table_mock(data, mock_map[key])
        f_opened.close()