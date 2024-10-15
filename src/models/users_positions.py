from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel
from src.utils.custom_types import uuid_pk


class UserPositionModel(BaseModel):
    __tablename__ = 'user_position'

    id: Mapped[uuid_pk]
    user_id: Mapped[uuid4] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'), primary_key=True,
    )
    position_id: Mapped[uuid4] = mapped_column(
        ForeignKey('position.id', ondelete='CASCADE'), primary_key=True,
    )
