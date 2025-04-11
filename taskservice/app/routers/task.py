from uuid import UUID
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user_id, get_task_service
from app.schemas.task import CreateTaskSchema, UpdateTaskSchema
from app.services.task import TaskService
from app.models.task import Status

task_router = APIRouter()


@task_router.post("/tasks")
async def create_task(
    create_task_schema: CreateTaskSchema,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await task_service.create_task(create_task_schema)


@task_router.post("/teams/{task_id}/users")
async def add_user(
    email: str,
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await task_service.add_user(task_id, email)


@task_router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    update_task_schema: UpdateTaskSchema,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await task_service.update_task(task_id, update_task_schema)


@task_router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await task_service.delete_task(task_id)

@task_router.post("/tasks/{task_id}/comments")
async def add_comment(
    task_id: int,
    text: str,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: UUID = Depends(get_current_user_id)
    ):
    return await task_service.add_comment(task_id, text)


@task_router.patch("/tasks/{task_id}")
async def change_status(
    task_id: int,
    status: Status,
    task_service: TaskService = Depends(get_task_service),
    current_user_id: UUID = Depends(get_current_user_id)
):
    return await task_service.change_status(task_id, status)