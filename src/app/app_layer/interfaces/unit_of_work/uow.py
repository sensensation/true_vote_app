from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from app.app_layer.interfaces.repositories.vote import AbstractVoteRepository

# from app.app_layer.interfaces.repositories.example_repo import AbstractExampleRepository


class AbcUnitOfWork(ABC):
    # List repositories below \/ to connect them in UoW
    # repo_example: AbcRepoExample

    vote_repo: AbstractVoteRepository

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

        await self.shutdown()

    @abstractmethod
    async def commit(self) -> None:
        """Commit changes"""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback cnagnes"""

    @abstractmethod
    async def shutdown(self) -> None:
        """Finish work with open sources"""
