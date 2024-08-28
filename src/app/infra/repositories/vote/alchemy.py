from sqlalchemy.ext.asyncio import AsyncSession

from app.app_layer.interfaces.repositories.vote import AbstractVoteRepository


class VoteRepository(AbstractVoteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    def create(self) -> None:
        # some realization
        ...
