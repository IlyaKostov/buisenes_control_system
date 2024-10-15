import datetime
import enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.response import BaseCreateResponse, BaseResponse
from src.schemas.user import UserDB


class TaskStatus(str, enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'
    ON_HOLD = 'On Hold'


class TaskID(BaseModel):
    id: UUID


class TaskBase(BaseModel):
    title: str
    description: str
    author_id: UUID
    responsible_id: Optional[UUID]
    deadline: datetime.datetime
    status: Optional[TaskStatus] = TaskStatus.OPEN
    time_estimate: str

    class Config:
        from_attributes = True


class CreateTask(TaskBase, BaseModel):
    assignees: List[UUID] = Field(default_factory=list)
    observers: List[UUID] = Field(default_factory=list)


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible_id: Optional[UUID] = None
    deadline: Optional[datetime.datetime] = None
    status: Optional[TaskStatus] = None
    time_estimate: Optional[str] = None
    assignees: Optional[List[UUID]] = Field(default_factory=list)
    observers: Optional[List[UUID]] = Field(default_factory=list)

    class Config:
        from_attributes = True


class TaskDB(TaskID, TaskBase):
    assignees: List[UserDB] = Field(default_factory=list)
    observers: List[UserDB] = Field(default_factory=list)


class TaskResponse(BaseCreateResponse):
    payload: TaskDB


class TaskUpdateResponse(BaseResponse):
    payload: TaskDB


class TaskResponseMessage(BaseResponse):
    message: str
