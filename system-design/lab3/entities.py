from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# class UserEntity(BaseModel):
#     id: int
#     username: str
#     password: str
#     firstname: str
#     lastname: str
#     email: str

# class OrderEntity(BaseModel):
#     id: int
#     name: str
#     description: str
#     user_id: int

# class TaskEntity(BaseModel):
#     id: int
#     name: str
#     description: str
#     order_id: int


class UserEntity(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)

class OrderEntity(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(String, index=True)

class TaskEntity(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    order_id = Column(String, index=True)
