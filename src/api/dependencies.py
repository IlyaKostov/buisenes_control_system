from typing import Annotated

from fastapi import Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request

from src.middleware.auth import oauth2_scheme
from src.models import AccountModel


async def get_current_account(request: Request, token: str = Depends(oauth2_scheme)) -> AccountModel:
    account = getattr(request.state, 'account', None)
    if account is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')
    return account


async def check_admin(account: AccountModel = Depends(get_current_account)) -> AccountModel:
    if not account.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not an admin')
    return account


CurrentAccount = Annotated[AccountModel, Depends(get_current_account)]
AdminAccount = Annotated[AccountModel, Depends(check_admin)]
