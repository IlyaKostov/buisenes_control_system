from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.schemas.account import AccountDB
from src.utils.custom_types import created_at, integer_pk, updated_at

if TYPE_CHECKING:
    from src.models import InviteModel, SecretModel, UserModel


class AccountModel(BaseModel):
    __tablename__ = 'account'

    id: Mapped[integer_pk]
    email: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['UserModel'] = relationship(back_populates='account', cascade='all, delete-orphan')
    invite: Mapped['InviteModel'] = relationship(back_populates='account', cascade='all, delete-orphan')
    secret: Mapped['SecretModel'] = relationship(back_populates='account', cascade='all, delete-orphan')

    def to_pydantic_schema(self) -> AccountDB:
        return AccountDB(**self.__dict__)
