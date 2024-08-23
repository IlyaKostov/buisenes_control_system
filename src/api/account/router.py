from fastapi import APIRouter, Depends

from src.api.account.service import AccountService
from src.schemas.account import CheckAccountResponse, CreateAccount, CreateAccountResponse, ConfirmAccount

router = APIRouter()


@router.get("/check_account/{account}")
async def check_and_create_account(
    account: CreateAccount,
    account_service: AccountService = Depends(AccountService),
):
    response_message: CreateAccountResponse = await account_service.check_and_create_account(account)

    return CheckAccountResponse(payload=response_message)


@router.post("/update-account")
async def update_account(account):
    pass
