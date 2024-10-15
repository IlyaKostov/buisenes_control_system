from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from src.models import AccountModel
from src.utils.auth.jwt import decode_jwt
from src.utils.unit_of_work import UnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/sign-in', auto_error=False)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, uow: UnitOfWork, excluded_routes: list | None = None) -> None:
        super().__init__(app)
        self.uow = uow
        self.excluded_routes = excluded_routes or []

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if any(request.url.path.startswith(routes) for routes in self.excluded_routes):
            return await call_next(request)

        try:
            token: str = await oauth2_scheme(request)

            if not token:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Authorization header missing')

            payload = decode_jwt(token=token)
            account_id = payload.get('sub')

            async with self.uow:
                account: AccountModel = await self.uow.account.get_account_by_id(_id=account_id)
                if not account:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Token invalid (account not found)',
                    )
                if not account.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='User inactive',
                    )

            request.state.account = account

        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token has expired')
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'invalid token error: {e}',
            )
        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code, content={'detail': http_exc.detail},
            )

        response: Response = await call_next(request)

        return response
