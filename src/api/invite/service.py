import random
import string

from src.models import InviteModel, AccountModel
from src.utils.base_service import BaseService
from src.utils.send_email import sending_email_with_invite_code
from src.utils.unit_of_work import transaction_mode


class InviteService(BaseService):
    base_repository = 'invite'

    @transaction_mode
    async def create_invite(self, account: AccountModel) -> InviteModel:
        invite_token: str = await self.generate_invite()

        invite: InviteModel = await self.uow.invite.add_one_and_get_obj(account_id=account.id, token=invite_token)

        # await sending_email_with_invite_code(account.email, invite_token)

        return invite

    @transaction_mode
    async def update_invite(self, account: AccountModel) -> InviteModel:
        new_token: str = await self.generate_invite()
        update_values: dict[str, str] = {'token': new_token}

        invite: InviteModel = await self.uow.invite.update_one_by_id(account.invite.id, update_values)

        # await sending_email_with_invite_code(account.email, new_token)

        return invite

    @staticmethod
    async def generate_invite(length: int = 5) -> str:
        return ''.join(random.choices(string.digits, k=length))

