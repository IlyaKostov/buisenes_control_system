from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.utils.custom_types import created_at, updated_at, uuid_pk

if TYPE_CHECKING:
    from src.models import AccountModel


class SecretModel(BaseModel):
    __tablename__ = 'secret'

    id: Mapped[uuid_pk]
    password: Mapped[bytes]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))

    account: Mapped['AccountModel'] = relationship(back_populates='secret')

    __table_args__ = (UniqueConstraint('account_id'),)
