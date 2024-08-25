import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import router
from src.metadata import DESCRIPTION, TAG_METADATA, TITLE, VERSION
from src.middleware.auth import AuthMiddleware
from src.utils.unit_of_work import UnitOfWork


def create_fast_api_app() -> FastAPI:
    load_dotenv(find_dotenv('.env'))
    env_name = os.getenv('MODE', 'DEV')

    excluded_paths = [
        "/api/account/check_account",
        "/api/auth/sign-up",
        "/api/auth/sign-up-complete",
        "/api/auth/sign-in",
        "/docs",
        "/redoc",
        "/openapi.json"
    ]

    if env_name != 'PROD':
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
        )
    else:
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            docs_url=None,
            redoc_url=None,
        )

    uow = UnitOfWork()
    fastapi_app.include_router(router, prefix='/api')
    fastapi_app.add_middleware(AuthMiddleware, uow=uow, excluded_routes=excluded_paths)
    return fastapi_app


app = create_fast_api_app()
