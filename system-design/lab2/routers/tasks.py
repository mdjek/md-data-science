from fastapi import APIRouter, Depends, HTTPException
from typing import List

from routers.auth import get_current_client
from entities import TaskEntity

router = APIRouter()

# Временное хранилище для услуг
tasks_db = []

# GET /tasks - Получить список услуг (требует аутентификации)
@router.get("/tasks", response_model=TaskEntity, dependencies=[Depends(get_current_client)])
def get_tasks(newTask: TaskEntity):
    for task in tasks_db:
        if task.id == newTask.id:
            raise HTTPException(status_code=404, detail="Task already exist")
    tasks_db.append(newTask)
    return newTask

# POST /tasks - Создать услугу (требует аутентификации)
@router.post("/tasks", response_model=TaskEntity, dependencies=[Depends(get_current_client)])
def create_task(newTask: TaskEntity):
    for order in tasks_db:
        if order.id == newTask.id:
            raise HTTPException(status_code=404, detail="Task already exist")
    tasks_db.append(newTask)
    return newTask

# PUT /tasks/{task_id} - Редактировать существующую услугу (требует аутентификации)
@router.put("/tasks/{task_id}", response_model=TaskEntity, dependencies=[Depends(get_current_client)])
def edit_task(task_id: str, updated_task: TaskEntity):
    for index, order in enumerate(tasks_db):
        if order.id == task_id:
            tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# GET /orders/{order_id}/tasks - Получить все услуги в заказе (требует аутентификации)
@router.get("/orders/{order_id}/tasks", response_model=TaskEntity, dependencies=[Depends(get_current_client)])
def get_tasks_for_order(order_id: int):
    current_tasks = []
    for task in tasks_db:
        if task.order_id == order_id:
            current_tasks.append(task)
    return current_tasks