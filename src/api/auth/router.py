from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.auth.service import AuthService
from src.middleware.auth import oauth2_scheme
from src.schemas.auth import AuthRequestSchema, TokenInfoSchema

router = APIRouter()


@router.post('/sign-in')
async def auth_user_issue_jwt(
    auth_request: AuthRequestSchema = Depends(AuthService().validate_auth_user),
    sign_in_service: AuthService = Depends(),
) -> TokenInfoSchema:
    token_info: TokenInfoSchema = await sign_in_service.sign_in(auth_request)
    return AuthResponseSchema(payload=token_info)
