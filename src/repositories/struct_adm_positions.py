import uuid

from sqlalchemy import select, Result

from src.models import StructAdmPositionModel
from src.utils.repository import SQLAlchemyRepository


class StructAdmPositionRepository(SQLAlchemyRepository):
    model = StructAdmPositionModel

    async def get_by_struct_and_position(self, department_id: int, position_id: uuid.UUID):
        stmt = (
            select(self.model)
            .filter_by(struct_adm_id=department_id, position_id=position_id)
        )
        result: Result = await self.session.execute(stmt)
        return result.scalars().first()
