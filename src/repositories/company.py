from src.utils.repository import SQLAlchemyRepository


class CompanyRepository(SQLAlchemyRepository):
    model = 'company'
