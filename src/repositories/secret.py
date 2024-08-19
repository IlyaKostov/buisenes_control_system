from src.utils.repository import SQLAlchemyRepository


class SecretRepository(SQLAlchemyRepository):
    model = 'secret'
