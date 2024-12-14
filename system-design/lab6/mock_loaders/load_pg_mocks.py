import json
from init_pg_db import SessionLocal
from entities import User, Order, Task

MODEL = User | Order | Task

MOCK_MAP = {
    # "users": User,
    "tasks": Task,
    "orders": Order
}

def loader(entity, modelEntity: MODEL):
    return modelEntity(**entity)


def load_pg_table_mock(data: list, modelEntity: MODEL):
    db = SessionLocal()

    collection = db.query(modelEntity).all()

    # если есть записи – не добавляем
    if len(collection):
        db.close()
        return

    for entity in data:
        # user = db.query(User).filter(User.username == username).first()n
        entityDB = loader(entity, modelEntity)

        db.add(entityDB)
        db.commit()

    db.close()


def load_pg_mock_data():
    for key in MOCK_MAP.keys():
        f_opened = open(f"./mocks/{key}.json")
        data = json.load(f_opened)

        load_pg_table_mock(data, MOCK_MAP[key])
        f_opened.close()