import uuid

from fastapi import APIRouter, Depends
from starlette import status

from src.api.tasks.service import TaskService
from src.api.dependencies import CurrentAccount
from src.models import TaskModel
from src.schemas.task import CreateTask, TaskResponse, UpdateTask, TaskResponseMessage, TaskUpdateResponse

router = APIRouter()


@router.post('/create-task', status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: CreateTask,
    account: CurrentAccount,
    task_service: TaskService = Depends(),
) -> TaskResponse:
    task: TaskModel = await task_service.create_task(task_data, account)
    return TaskResponse(payload=task.to_pydantic_schema())


@router.put('/tasks/{task_id}')
async def update_task(
    task_id: uuid.UUID,
    task_data: UpdateTask,
    account: CurrentAccount,
    task_service: TaskService = Depends()
) -> TaskUpdateResponse:
    task: TaskModel = await task_service.update_task(task_id, task_data, account)
    return TaskUpdateResponse(payload=task.to_pydantic_schema())


@router.delete('/tasks/{task_id}')
async def delete_task(
    task_id: uuid.UUID,
    account: CurrentAccount,
    task_service: TaskService = Depends()
) -> TaskResponseMessage:
    await task_service.delete_task(task_id, account)
    return TaskResponseMessage(message='Task deleted successfully.')