from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, DateTime, Identity
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Users models 
class CreateUserEntity(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str

class ResponseUserEntity(CreateUserEntity):
    id: int

    class Config:
        from_attributes = True

# Orders models
class CreateOrderEntity(BaseModel):
    name: str
    description: str
    user_id: int

class ResponseOrderEntity(CreateOrderEntity):
    id: int

# Task models
class CreateTaskEntity(BaseModel):    
    name: str
    description: str
    order_id: int

class ResponseTaskEntity(CreateTaskEntity):
    id: int

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, index=True)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    order_id = Column(Integer, index=True)
