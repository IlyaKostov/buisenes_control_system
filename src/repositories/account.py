from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.models import AccountModel
from src.utils.repository import SQLAlchemyRepository


class AccountRepository(SQLAlchemyRepository):
    model = AccountModel

    async def get_account_by_email(self, email: str):
        stmt = (
            select(self.model)
            .options(joinedload(self.model.secret), joinedload(self.model.user), joinedload(self.model.invite))
            .filter_by(email=email)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_account_by_id(self, _id: int):
        stmt = (
            select(self.model)
            .options(joinedload(self.model.secret), joinedload(self.model.user), joinedload(self.model.invite))
            .filter_by(id=_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
