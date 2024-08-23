import random
import string

from starlette import status
from starlette.exceptions import HTTPException

from src.schemas.account import CreateAccount, CreateAccountResponse, ConfirmAccount
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class AccountService(BaseService):
    base_repository = 'account'

    @transaction_mode
    async def check_and_create_account(self, check_account: CreateAccount) -> CreateAccountResponse:
        account = await self.uow.account.get_account_by_email(check_account.email)
        if account.user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

        new_account = self.uow.account.add_one_and_get_obj(email=check_account.email)
        invite_token = self.generate_invite()
        invite = self.uow.invite.add_one_and_get_obj(invite_token=invite_token)

        new_account.invite = invite

        return CreateAccountResponse(message="Email is available, Invite code sent")

    @transaction_mode
    async def check_account_invite(self, confirm_account: ConfirmAccount) -> CreateAccountResponse:
        account = await self.uow.account.get_account_by_email(confirm_account.email)
        if account.invite.token != confirm_account.token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account or invite token.")
        return CreateAccountResponse(message="Email confirmed.")

    @staticmethod
    async def generate_invite(length=5):
        return ''.join(random.choices(string.digits, k=length))
