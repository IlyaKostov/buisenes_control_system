from src.schemas.account import SignUpCompleteRequest
from src.schemas.company import CompanyDB
from src.utils.auth.password import hash_password
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class CompanyService(BaseService):
    base_repository = 'company'

    @transaction_mode
    async def create_company(self, complete_data: SignUpCompleteRequest) -> CompanyDB:

        account = await self.uow.account.get_account_by_email(complete_data.email)

        new_company = await self.uow.company.add_one_and_get_obj(
            inn=complete_data.inn,
            company_name=complete_data.company_name,
        )

        new_user = await self.uow.user.add_one_and_get_obj(
            first_name=complete_data.first_name,
            last_name=complete_data.last_name,
            middle_name=complete_data.middle_name,
            account_id=account.id,
            company_id=new_company.id
        )

        hashed_password = hash_password(complete_data.password)

        secret = await self.uow.secret.add_one_and_get_obj(password=hashed_password, account_id=account.id)

        account.secret = secret
        account.user = new_user
        account.is_admin = True

        return CompanyDB(
            id=new_company.id,
            inn=new_company.inn,
            company_name=new_company.company_name,
            is_active=True
        )
