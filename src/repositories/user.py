import uuid

from sqlalchemy import select, Result

from src.models import UserModel
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel

    async def get_object_by_ids(self, users_ids: list[uuid.UUID]) -> list[UserModel]:
        stmt = (
            select(self.model)
            .filter(self.model.id.in_(users_ids))
        )
        result: Result = await self.session.execute(stmt)
        return list(result.scalars().all())
