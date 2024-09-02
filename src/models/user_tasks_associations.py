from sqlalchemy import Table, Column, ForeignKey, UUID

from src.models import BaseModel

task_observers = Table(
    'task_observers', BaseModel.metadata,
    Column('task_id', UUID(as_uuid=True), ForeignKey('task.id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)
)

task_assignees = Table(
    'task_assignees', BaseModel.metadata,
    Column('task_id', UUID(as_uuid=True), ForeignKey('task.id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)
)