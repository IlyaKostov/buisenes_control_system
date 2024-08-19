from src.utils.repository import SQLAlchemyRepository


class AccountRepository(SQLAlchemyRepository):
    model = 'account'
