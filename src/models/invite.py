from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.utils.custom_types import uuid_pk

if TYPE_CHECKING:
    from src.models.account import AccountModel


class InviteModel(BaseModel):
    __tablename__ = 'invite'

    id: Mapped[uuid_pk]
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    token: Mapped[str] = mapped_column(String(30))

    account: Mapped['AccountModel'] = relationship(back_populates='user', cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('account_id'),)
