from fastapi import FastAPI
# from routers import auth, users, orders, tasks
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.orm import sessionmaker, Session
from entities import Base

# Настройка PostgreSQL
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db_profi/profi"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# Настройка SQLAlchemy
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/postgres")

# DATABASE_URL = "postgresql://postgres:postgres@db_profi"
# DATABASE_URL = "postgresql://postgres:pass@db_profi:5433/profi"
DATABASE_URL = "postgresql://postgres:pass@db/profi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # # Создание таблиц
Base.metadata.create_all(bind=engine)

# Инициализация приложения
app = FastAPI(title="App", description="API для управления заказами/услугами")

# app.include_router(auth.router)
# app.include_router(users.router)
# app.include_router(orders.router)
# app.include_router(tasks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)