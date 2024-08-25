from datetime import datetime, UTC

from fastapi import Form
from starlette import status
from starlette.exceptions import HTTPException

from src.schemas.auth import TokenInfoSchema, AuthRequestSchema
from src.utils.auth.jwt import encode_jwt
from src.utils.auth.password import validate_password
from src.utils.base_service import BaseService
from src.utils.unit_of_work import transaction_mode


class AuthService(BaseService):

    async def sign_in(self, auth_request: AuthRequestSchema) -> TokenInfoSchema:
        current_time = datetime.now(UTC)
        jwt_payload = {
            "sub": auth_request.id,
            "email": auth_request.email,
            "logged_in_at": current_time.timestamp()
        }
        token = encode_jwt(jwt_payload)
        return TokenInfoSchema(
            access_token=token,
            token_type="Bearer"
        )

    @transaction_mode
    async def validate_auth_user(
            self,
            username: str = Form(),
            password: str = Form(),
    ):
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
        )

        account = await self.uow.account.get_account_by_email(email=username)
        if not account:
            raise unauthed_exc

        if not validate_password(
                password=password,
                hashed_password=account.secret.password,
        ):
            raise unauthed_exc

        if not account.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="account inactive",
            )

        return account
