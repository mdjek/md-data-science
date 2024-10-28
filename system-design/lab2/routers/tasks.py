from fastapi import APIRouter, Depends, Form, HTTPException
from typing import Dict, Optional, List

from routers.auth import get_current_client
from entities import TaskEntity

router = APIRouter()

# Временное хранилище для услуг
tasks_db = []

# GET /tasks - Получить список услуг (требует аутентификации)
@router.get("/tasks", response_model=List[TaskEntity])
def get_tasks(newTask: TaskEntity, current_user: str = Depends(get_current_client)):
    for task in tasks_db:
        if task.id == newTask.id:
            raise HTTPException(status_code=404, detail="Task already exist")
    tasks_db.append(newTask)
    return newTask

# POST /tasks - Создать услугу (требует аутентификации)
@router.post("/tasks", response_model=List[TaskEntity])
def create_task(newTask: TaskEntity, current_user: str = Depends(get_current_client)):
    for order in tasks_db:
        if order.id == newTask.id:
            raise HTTPException(status_code=404, detail="Task already exist")
    tasks_db.append(newTask)
    return newTask

# PUT /tasks/{task_id} - Редактировать существующую услугу (требует аутентификации)
@router.put("/tasks/{task_id}", response_model=List[TaskEntity])
def edit_task(task_id: str, updated_task: TaskEntity, current_user: str = Depends(get_current_client)):
    for index, order in enumerate(tasks_db):
        if order.id == task_id:
            tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# GET /orders/{order_id}/tasks - Получить все услуги в заказе (требует аутентификации)
@router.get("/orders/{order_id}/tasks", response_model=TaskEntity)
def get_tasks_for_order(order_id: int, current_user: str = Depends(get_current_client)):
    current_tasks = []
    for task in tasks_db:
        if task.order_id == order_id:
            current_tasks.append(task)
    return current_tasks