from src.utils.repository import SQLAlchemyRepository


class InviteRepository(SQLAlchemyRepository):
    model = 'invite'
