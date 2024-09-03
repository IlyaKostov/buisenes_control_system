import uuid

from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload

from src.models import PositionModel
from src.utils.repository import SQLAlchemyRepository


class PositionRepository(SQLAlchemyRepository):
    model = PositionModel

    async def get_position_with_users(self, position_id: uuid.UUID):
        stmt = (
            select(self.model)
            .options(selectinload(self.model.users))
            .filter_by(id=position_id)
        )
        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
