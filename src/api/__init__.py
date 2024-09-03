__all__ = [
    'router',
]

import asyncio

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from src.api.account.router import router as account_router
from src.api.auth.router import router as auth_router
from src.api.company.router import router as company_router
from src.api.positions.router import router as position_router
from src.api.struct_adm.router import router as department_router
from src.api.users.router import router as users_router
from src.database.db import get_async_session
from src.metadata import ERRORS_MAP
from src.schemas.response import BaseResponse

router = APIRouter()
router.include_router(account_router, prefix='/account', tags=['Account | v1'])
router.include_router(auth_router, prefix='/auth', tags=['Auth | v1'])
router.include_router(company_router, prefix='/company', tags=['Auth | v1'])
router.include_router(users_router, prefix='/users', tags=['User | v1'])
router.include_router(department_router, prefix='/department', tags=['Department | v1'])
router.include_router(position_router, prefix='/position', tags=['Position | v1'])


@router.get(
    path='/healthz/',
    tags=['healthz'],
    status_code=HTTP_200_OK,
)
async def health_check(
        session: AsyncSession = Depends(get_async_session),
) -> BaseResponse:
    """Check api external connection."""
    async def check_service(service: str) -> None:
        try:
            if service == 'postgres':
                await session.execute(text('SELECT 1'))
        except Exception as exc:
            logger.error(f'Health check failed with error: {exc}')
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ERRORS_MAP.get(service))

    await asyncio.gather(*[
        check_service('postgres'),
    ])

    return BaseResponse()
