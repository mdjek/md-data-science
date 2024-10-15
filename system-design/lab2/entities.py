from pydantic import BaseModel, Field

class UserEntity(BaseModel):
    id: int = None
    username: str
    password: str
    first_name: str
    last_name: str
    email: str

class OrderEntity(BaseModel):
    id: int = None
    name: str
    description: str

class TaskEntity(BaseModel):
    id: int = None
    name: str
    description: str