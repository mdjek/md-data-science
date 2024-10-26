from pydantic import BaseModel, Field

class UserEntity(BaseModel):
    id: int
    username: str
    password: str
    firstname: str
    lastname: str
    email: str

class OrderEntity(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

class TaskEntity(BaseModel):
    id: int
    name: str
    description: str
    order_id: int