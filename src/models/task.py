import datetime
import enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.utils.custom_types import uuid_pk

if TYPE_CHECKING:
    from src.models import UserModel


class TaskStatus(str, enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'
    ON_HOLD = 'On Hold'


class TaskModel(BaseModel):
    __tablename__ = 'task'

    id: Mapped[uuid_pk]
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str]
    author_id: Mapped[uuid4] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
    )
    responsible_id: Mapped[uuid4] = mapped_column(
        ForeignKey('user.id', ondelete='SET NULL'),
    )
    deadline: Mapped[datetime.datetime]
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus, native_enum=False), default=TaskStatus.OPEN)
    time_estimate: Mapped[str]

    author: Mapped['UserModel'] = relationship(
        foreign_keys=[author_id], overlaps='observers,assignees',
    )
    responsible: Mapped['UserModel'] = relationship(
        foreign_keys=[responsible_id], overlaps='observers,assignees',
    )

    observers: Mapped[list['UserModel']] = relationship(secondary='task_observers')
    assignees: Mapped[list['UserModel']] = relationship(secondary='task_assignees')
