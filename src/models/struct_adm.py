from typing import TYPE_CHECKING, Any, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship, remote
from sqlalchemy_utils import LtreeType

from src.models.base import BaseModel
from src.models.mixins.company_mixin import CompanyMixin
from src.schemas.struc_adm import StructAdmDB
from src.utils.custom_types import integer_pk

if TYPE_CHECKING:
    from src.models import PositionModel, UserModel


class StructAdmModel(CompanyMixin, BaseModel):
    __tablename__ = 'struct_adm'

    _company_back_populates: str | None = 'structs_adm'

    id: Mapped[integer_pk]
    name: Mapped[str] = mapped_column(String(50))
    path: Mapped[Any] = mapped_column(LtreeType)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('struct_adm.id', ondelete='CASCADE'))
    manager_id: Mapped[Optional[uuid4]] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))

    parent: Mapped['StructAdmModel'] = relationship(
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref='children',
        viewonly=True,
    )

    manager: Mapped['UserModel'] = relationship(foreign_keys=[manager_id])

    positions: Mapped[list['PositionModel']] = relationship(
        secondary='struct_adm_position', back_populates='structs_adm',
    )

    __table_args__ = (
        Index('ix_struct_adm_path', path, postgresql_using='gist'),
    )

    def to_pydantic_schema(self) -> StructAdmDB:
        return StructAdmDB(**self.__dict__)
