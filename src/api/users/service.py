from pydantic import EmailStr
from starlette import status
from starlette.exceptions import HTTPException

from src.models import AccountModel, UserModel
from src.schemas.user import CreateUserRequest, UpdateUserRequest
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository = 'user'

    @transaction_mode
    async def create_user(
            self,
            email: EmailStr,
            request_user: CreateUserRequest,
            admin_account: AccountModel,
    ) -> UserModel:
        account: AccountModel = await self.uow.account.get_account_by_email(email)
        if account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email')

        new_user: UserModel = await self.uow.user.add_one_and_get_obj(
            first_name=request_user.first_name,
            last_name=request_user.last_name,
            middle_name=request_user.middle_name,
            account_id=account.id,
            company_id=admin_account.user.company_id,
        )
        account.user = new_user
        return new_user

    @transaction_mode
    async def update_user(
            self,
            request_user: UpdateUserRequest,
            account: AccountModel,
    ) -> UserModel:

        updates: dict[str, str] = {
            'first_name': request_user.first_name,
            'last_name': request_user.last_name,
            'middle_name': request_user.middle_name,
        }

        updates = {k: v for k, v in updates.items() if v is not None}

        if not updates:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No fields to update')

        updated_user: UserModel = await self.uow.user.update_one_by_id(account.user.id, values=updates)

        return updated_user
