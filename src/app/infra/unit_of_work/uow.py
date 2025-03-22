from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.infra.repositories.room.alchemy import RoomRepository
from app.infra.repositories.vote.alchemy import VoteRepository


class Uow(AbcUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self) -> "AbcUnitOfWork":  # type: ignore[override]
        self.session = self.session_factory()

        # self.example_repo = ExampleRepository(self.session)
        self.vote_repo = VoteRepository(self.session)
        self.rooms_repo = RoomRepository(self.session)

        return await super().__aenter__()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def shutdown(self) -> None:
        await self.session.close()
