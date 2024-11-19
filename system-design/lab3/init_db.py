import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities import Base, Task, Order, ResponseUserEntity, ResponseOrderEntity

DATABASE_URL = "postgresql://postgres:pass@db/profi_db"
engine = create_engine(DATABASE_URL, echo = True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Зависимости для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()