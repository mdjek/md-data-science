from fastapi import APIRouter, Depends, HTTPException
from typing import List
from routers.auth import get_current_client
from entities import ResponseTaskEntity, CreateTaskEntity, Task
from init_db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# GET /tasks - Получить список услуг (требует аутентификации)
# @router.get("/tasks", response_model=List[ResponseTaskEntity], tags=["Tasks"], dependencies=[Depends(get_current_client)])
@router.get("/tasks", response_model=List[ResponseTaskEntity], tags=["Tasks"])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# POST /tasks - Создать услугу (требует аутентификации)
# @router.post("/tasks", response_model=ResponseTaskEntity, tags=["Tasks"], dependencies=[Depends(get_current_client)])
@router.post("/tasks", response_model=ResponseTaskEntity, tags=["Tasks"])
def create_task(new_task: CreateTaskEntity, db: Session = Depends(get_db)):
    if db.query(Task).filter(Task.name == new_task.name).first():
        raise HTTPException(status_code=404, detail="Task with such name already exist")

    db_order = Task(**new_task.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# PUT /tasks/{task_id} - Редактировать существующую услугу (требует аутентификации)
# @router.put("/tasks/{task_id}", response_model=ResponseTaskEntity, tags=["Tasks"], dependencies=[Depends(get_current_client)])
@router.put("/tasks/{task_id}", response_model=ResponseTaskEntity, tags=["Tasks"])
def edit_task(task_id: int, updated_task: CreateTaskEntity, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if task:
        task.name = updated_task.name if isinstance(updated_task.name, str) else task.name
        task.description = updated_task.description if isinstance(updated_task.description, str) else task.description
        task.order_id = updated_task.order_id if isinstance(updated_task.order_id, int) else task.order_id
        
        db.commit()
        db.refresh(task)
        return task
    
    raise HTTPException(status_code=404, detail="Task not found")

# GET /orders/{order_id}/tasks - Получить все услуги в заказе (требует аутентификации)
# @router.get("/orders/{order_id}/tasks", response_model=ResponseTaskEntity, tags=["Tasks"], dependencies=[Depends(get_current_client)])
@router.get("/orders/{order_id}/tasks", response_model=List[ResponseTaskEntity], tags=["Tasks"])
def get_tasks_for_order(order_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.order_id == order_id).all()

    if tasks:
        return tasks

    raise HTTPException(status_code=404, detail="Tasks not found")