import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import TaskModel
from src.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = TaskModel

    async def get_task_with_assignees_and_observers(self, task_id: uuid.UUID):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.assignees), selectinload(self.model.observers))
            .filter_by(id=task_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
