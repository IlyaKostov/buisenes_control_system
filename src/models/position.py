from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import BaseModel

from typing import TYPE_CHECKING

from src.utils.custom_types import uuid_pk

if TYPE_CHECKING:
    from src.models import UserModel, StructAdmModel


class PositionModel(BaseModel):
    __tablename__ = "position"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(String(50))

    users: Mapped[list["UserModel"]] = relationship(
        secondary="user_position", back_populates="positions"
    )

    structs_adm: Mapped[list["StructAdmModel"]] = relationship(
        secondary="struct_adm_position", back_populates="positions"
    )
