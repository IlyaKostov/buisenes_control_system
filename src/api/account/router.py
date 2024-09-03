from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import EmailStr
from starlette import status
from starlette.exceptions import HTTPException

from src.api.dependencies import CurrentAccount
from src.api.account.service import AccountService
from src.models import AccountModel
from src.schemas.account import CheckAccountResponse, CreateAccountResponse, UpdateAccountResponse
from src.schemas.auth import AuthRequestSchema

router = APIRouter()


@router.get("/check_account/{account}")
async def check_and_create_account(
    account: EmailStr,
    background_tasks: BackgroundTasks,
    account_service: AccountService = Depends(),
) -> CheckAccountResponse:
    response_message: CreateAccountResponse = await account_service.check_and_create_account(account, background_tasks)

    return CheckAccountResponse(payload=response_message)


@router.post("/create-account")
async def create_account(
    account: CurrentAccount,
    email: EmailStr,
    background_tasks: BackgroundTasks,
    account_service: AccountService = Depends(),
) -> CheckAccountResponse:

    if not account.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User don't have permission to create'")

    response_message: CreateAccountResponse = await account_service.check_and_create_account(email, background_tasks)
    return CheckAccountResponse(payload=response_message)


@router.post("/confirm-account")
async def confirm_account(
    confirmed_data: AuthRequestSchema,
    account_service: AccountService = Depends(),
) -> CheckAccountResponse:

    response_message: CreateAccountResponse = await account_service.confirm_account(confirmed_data)

    return CheckAccountResponse(payload=response_message)


@router.put("/change-email")
async def change_email(
    account: CurrentAccount,
    email: EmailStr,
    account_service: AccountService = Depends(AccountService),
) -> UpdateAccountResponse:
    account: AccountModel = await account_service.change_email(email, account)
    return UpdateAccountResponse(payload=account.to_pydantic_schema())
