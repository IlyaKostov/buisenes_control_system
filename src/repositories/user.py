from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = 'user'
