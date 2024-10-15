from fastapi import APIRouter, Depends
from pydantic import EmailStr
from starlette import status
from starlette.exceptions import HTTPException

from src.api.dependencies import CurrentAccount
from src.api.users.service import UserService
from src.models import UserModel
from src.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
    UpdateUserResponse
)
router = APIRouter()


@router.post('/create-user')
async def create_user(
        account: CurrentAccount,
        email: EmailStr,
        request_user: CreateUserRequest,
        user_service: UserService = Depends(),
) -> CreateUserResponse:

    if not account.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User don't have permission to create'")

    user: UserModel = await user_service.create_user(email, request_user, account)
    return CreateUserResponse(payload=user.to_pydantic_schema())


@router.put('/update-user')
async def update_account(
        account: CurrentAccount,
        request_user: UpdateUserRequest,
        user_service: UserService = Depends(),
) -> UpdateUserResponse:

    user: UserModel = await user_service.update_user(request_user, account)
    return UpdateUserResponse(payload=user.to_pydantic_schema())
