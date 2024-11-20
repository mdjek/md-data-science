from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Users models (mongo db) 
class CreateUserEntity(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str

class ResponseUserEntity(CreateUserEntity):
    id: int

# Orders models (pg db)
class CreateOrderEntity(BaseModel):
    name: str
    description: str
    user_id: int

class ResponseOrderEntity(CreateOrderEntity):
    id: int

# Task models (pg db)
class CreateTaskEntity(BaseModel):    
    name: str
    description: str
    order_id: int

class ResponseTaskEntity(CreateTaskEntity):
    id: int

# Pg models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True)
    password = Column(String)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, index=True)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    order_id = Column(Integer, index=True)

# Mongo models