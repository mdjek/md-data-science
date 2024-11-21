import json
from init_pg_db import SessionLocal
from entities import User, Order, Task

MODEL = User | Order | Task

def loader(entity, modelEntity: MODEL):
    return modelEntity(**entity)


def load_pg_table_mock(data: list, modelEntity: MODEL):
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