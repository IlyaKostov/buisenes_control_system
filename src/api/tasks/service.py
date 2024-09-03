import datetime
import uuid

from starlette import status
from starlette.exceptions import HTTPException

from src.models import TaskModel, AccountModel
from src.schemas.task import CreateTask, UpdateTask, TaskStatus
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class TaskService(BaseService):
    base_repository = 'task'

    @transaction_mode
    async def create_task(self, task_data: CreateTask, account: AccountModel) -> TaskModel:

        observers_list = await self.uow.user.get_object_by_ids(task_data.observers)
        assignees_list = await self.uow.user.get_object_by_ids(task_data.assignees)

        task: TaskModel = await self.uow.task.add_one_and_get_obj(
            title=task_data.title,
            description=task_data.description,
            author_id=task_data.author_id,
            responsible_id=task_data.responsible_id,
            deadline=task_data.deadline,
            status=task_data.status,
            time_estimate=task_data.time_estimate,
        )
        await self.uow.commit()
        await self.uow.session.refresh(task)

        task = await self.uow.task.get_task_with_assignees_and_observers(task.id)
        task.observers = observers_list
        task.assignees = assignees_list

        return task

    @transaction_mode
    async def update_task(
        self,
        task_id: uuid.UUID,
        task_data: UpdateTask,
        account: AccountModel
    ) -> TaskModel:
        task: TaskModel = await self.uow.task.get_task_with_assignees_and_observers(task_id)

        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

        await self._update_fields(task, task_data)

        return task

    @transaction_mode
    async def delete_task(self, task_id: uuid.UUID, account: AccountModel) -> None:
        task: TaskModel = await self.uow.task.get_task_with_assignees_and_observers(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")

        await self.uow.task.delete_by_query(id=task_id)

    async def _update_fields(self, task: TaskModel, task_data: UpdateTask):
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description

        await self._update_deadline(task, task_data.deadline)
        await self._update_status(task, task_data.status)
        await self._update_responsible(task, task_data.responsible_id)
        await self._update_users(task, 'observers', task_data.observers)
        await self._update_users(task, 'assignees', task_data.assignees)

    @staticmethod
    async def _update_deadline(task: TaskModel, deadline: datetime.datetime):
        if deadline is not None:
            if deadline < datetime.datetime.now():
                raise HTTPException(status_code=400, detail="Deadline must be in the future.")
            task.deadline = deadline

    @staticmethod
    async def _update_status(task: TaskModel, task_status: TaskStatus):
        if task_status is not None:
            allowed_statuses = [TaskStatus.OPEN, TaskStatus.IN_PROGRESS, TaskStatus.CLOSED, TaskStatus.ON_HOLD]
            if task_status not in allowed_statuses:
                raise HTTPException(status_code=400, detail="Invalid status for the task.")
            task.status = task_status

    async def _update_responsible(self, task: TaskModel, responsible_id: uuid.UUID):
        if responsible_id is not None:
            responsible_user = await self.uow.user.get_by_query_one_or_none(id=responsible_id)
            if not responsible_user:
                raise HTTPException(status_code=404, detail="Responsible user does not exist.")
            task.responsible_id = responsible_id

    async def _update_users(self, task: TaskModel, field: str, user_ids: list):
        if user_ids is not None:
            users = await self.uow.user.get_object_by_ids(user_ids)
            setattr(task, field, users)
