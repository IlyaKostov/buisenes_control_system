from uuid import uuid4

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.models import BaseModel
from src.utils.custom_types import uuid_pk


class StructAdmPositionModel(BaseModel):
    __tablename__ = "struct_adm_position"
    __table_args__ = (
        UniqueConstraint('struct_adm_id', 'position_id', name='idx_unique_struct_adm_position'),
    )

    id: Mapped[uuid_pk]

    struct_adm_id: Mapped[uuid4] = mapped_column(
        ForeignKey("struct_adm.id", ondelete="CASCADE")
    )

    position_id: Mapped[uuid4] = mapped_column(
        ForeignKey("position.id", ondelete="CASCADE")
    )

