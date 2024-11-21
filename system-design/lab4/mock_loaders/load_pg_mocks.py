import json
from init_pg_db import SessionLocal
from entities import User, Order, Task
from typing import Callable

def load_pg_user(entity):
    return User(
        username=entity["username"],
        first_name=entity["first_name"],
        last_name=entity["last_name"],
        email=entity["email"],
        password=entity["password"]
    )

def load_pg_order(entity):
    return Order(
        name=entity["name"],
        description=entity["description"],
        user_id=entity["user_id"],
    )

def load_pg_task(entity):
    return Task(
        name=entity["name"],
        description=entity["description"],
        order_id=entity["order_id"],
    )

def loader(entity, modelEntity: User | Order | Task):
    return modelEntity(**entity)


def load_pg_table_mock(data: list, modelEntity: User | Order | Task):
    db = SessionLocal()

    for entity in data:
        # user = db.query(User).filter(User.username == username).first()n
        entityDB = loader(entity, modelEntity)

        db.add(entityDB)
        db.commit()

    db.close()

def load_pg_mock_data():
    mock_map = {
        # "users": User,
        "tasks": Task,
        "orders": Order
    }

    for key in mock_map.keys():
        f_opened = open(f"./mocks/{key}.json")
        data = json.load(f_opened)

        load_pg_table_mock(data, mock_map[key])
        f_opened.close()