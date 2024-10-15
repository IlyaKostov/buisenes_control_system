from fastapi import BackgroundTasks
from pydantic import EmailStr
from starlette import status
from starlette.exceptions import HTTPException

from src.api.invite.service import InviteService
from src.models import AccountModel
from src.schemas.account import ConfirmAccount, CreateAccountResponse
from src.schemas.auth import AuthRequestSchema
from src.utils.auth.password import hash_password
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class AccountService(BaseService):
    base_repository = 'account'

    @transaction_mode
    async def check_and_create_account(
        self,
        email: EmailStr,
        background_tasks: BackgroundTasks
    ) -> CreateAccountResponse:
        account: AccountModel = await self.uow.account.get_account_by_email(email)
        invite_service = InviteService()

        if account and account.user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already in use')

        if account is None:
            account = await self.uow.account.add_one_and_get_obj(email=email)
            await self.uow.commit()
            invite = await invite_service.create_invite(account, background_tasks)
            account.invite = invite
        elif account and account.invite:
            await invite_service.update_invite(account, background_tasks)
        else:
            invite = await invite_service.create_invite(account, background_tasks)
            account.invite = invite

        return CreateAccountResponse(message='Email is available, Invite link sent')

    @transaction_mode
    async def check_account_invite(self, confirm_account: ConfirmAccount) -> CreateAccountResponse:
        account = await self.uow.account.get_account_by_email(confirm_account.email)

        if account is None or not account.invite or account.invite.token != confirm_account.token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid account or invite token.')

        return CreateAccountResponse(message='Email confirmed.')

    @transaction_mode
    async def confirm_account(self, confirm_data: AuthRequestSchema) -> CreateAccountResponse:
        account = await self.uow.account.get_account_by_email(confirm_data.email)
        if account is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid account')

        hashed_password = hash_password(confirm_data.password)

        secret = await self.uow.secret.add_one_and_get_obj(password=hashed_password, account_id=account.id)
        account.secret = secret
        return CreateAccountResponse(message='Email confirmed and set password')

    @transaction_mode
    async def change_email(self, email: EmailStr, account_data: AccountModel) -> AccountModel:
        account: AccountModel = await self.uow.account.get_account_by_email(email)

        if account:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already in use')

        updated_data: dict[str, str] = {
            'email': email,
        }

        updated_account: AccountModel = await self.uow.account.update_one_by_id(account_data.id, updated_data)

        return updated_account
