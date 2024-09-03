import functools
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any

from src.database.db import async_session_maker

from src.repositories import (
    AccountRepository,
    CompanyRepository,
    InviteRepository,
    SecretRepository,
    UserRepository,
)
from src.repositories.position import PositionRepository
from src.repositories.struct_adm import StructAdmRepository
from src.repositories.struct_adm_positions import StructAdmPositionRepository
from src.repositories.task import TaskRepository
from src.utils.custom_types import async_func


class AbstractUnitOfWork(ABC):
    user: UserRepository
    account: AccountRepository
    invite: InviteRepository
    company: CompanyRepository
    secret: SecretRepository
    task: TaskRepository
    position: PositionRepository
    struct_adm: StructAdmRepository
    struct_adm_position: StructAdmPositionRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions"""

    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        self.account = AccountRepository(self.session)
        self.invite = InviteRepository(self.session)
        self.company = CompanyRepository(self.session)
        self.secret = SecretRepository(self.session)
        self.task = TaskRepository(self.session)
        self.position = PositionRepository(self.session)
        self.struct_adm = StructAdmRepository(self.session)
        self.struct_adm_position = StructAdmPositionRepository(self.session)

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


def transaction_mode(func: async_func) -> async_func:
    """Decorate a function with transaction mode."""
    @functools.wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
