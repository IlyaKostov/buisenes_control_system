from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, ExpiredSignatureError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.utils.auth.jwt import decode_jwt
from src.utils.unit_of_work import UnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, uow: UnitOfWork, excluded_routes: list | None = None):
        super().__init__(app)
        self.uow = uow
        self.excluded_routes = excluded_routes or []

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.excluded_routes:
            return await call_next(request)

        token = await oauth2_scheme(request)
        if not token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authorization header missing")

        try:
            payload = decode_jwt(token=token)
            account_id = payload.get("sub")

            async with self.uow as uow:
                account = await uow.account.get_by_query_one_or_none(id=account_id)
                if not account:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token invalid (account not found)",
                    )
                if not account.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="User inactive",
                    )
                request.state.account = account

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired")
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token error: {e}",
            )

        response = await call_next(request)

        return response
