from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.utils.custom_types import integer_pk, created_at, updated_at

if TYPE_CHECKING:
    from src.models import UserModel, SecretModel, InviteModel


class AccountModel(BaseModel):
    __tablename__ = 'account'

    id: Mapped[integer_pk]
    email: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped['UserModel'] = relationship(back_populates='account')
    invite: Mapped['InviteModel'] = relationship(back_populates='account')
    secret: Mapped['SecretModel'] = relationship(back_populates='account')
