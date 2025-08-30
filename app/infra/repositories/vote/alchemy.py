from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app_layer.interfaces.repositories.vote import AbstractVoteRepository
from app.domain.votes.dto import VoteDTO
from app.domain.votes.entities import VoteEntity
from app.domain.votes.enums import VoteStatusEnum
from app.infra.db.models import VoteORM


class VoteRepository(AbstractVoteRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, vote: VoteEntity) -> VoteEntity:
        """Create new vote and return created entity."""
        db_vote = VoteORM(
            id=vote.data.id,
            user_id=vote.data.user_id,
            option_id=vote.data.option_id,
            room_id=vote.data.room_id,
            status=vote.data.status,
            meta=vote.data.meta,
            blockchain_txn_id=vote.data.blockchain_txn_id,
        )
        self._session.add(db_vote)
        await self._session.commit()
        await self._session.refresh(db_vote)

        return VoteEntity(VoteDTO.model_validate(db_vote, from_attributes=True))

    async def get_by_user_and_room(self, user_id: UUID, room_id: UUID) -> VoteEntity | None:
        """Get vote by user_id and room_id."""
        stmt = select(VoteORM).where(
            and_(
                VoteORM.user_id == user_id,
                VoteORM.room_id == room_id,
            ),
        )
        row = await self._session.scalar(stmt)

        if not row:
            return None

        return VoteEntity(VoteDTO.model_validate(row, from_attributes=True))

    async def get_by_id(self, vote_id: UUID) -> VoteEntity | None:
        """Get vote by id."""
        stmt = select(VoteORM).where(VoteORM.id == vote_id)
        row = await self._session.scalar(stmt)

        if not row:
            return None

        return VoteEntity(VoteDTO.model_validate(row, from_attributes=True))

    async def get_by_room(self, room_id: UUID, statuses: list[VoteStatusEnum] | None = None) -> list[VoteEntity]:
        """Get all votes for room with optional status filter."""
        stmt = select(VoteORM).where(
            and_(
                VoteORM.room_id == room_id,
                VoteORM.status.in_(statuses or list(VoteStatusEnum)),
            ),
        )
        rows = (await self._session.scalars(stmt)).all()

        return [VoteEntity(VoteDTO.model_validate(row, from_attributes=True)) for row in rows]

    async def get_by_user(self, user_id: UUID, statuses: list[VoteStatusEnum] | None = None) -> list[VoteEntity]:
        """Get all votes for user with optional status filter."""
        stmt = select(VoteORM).where(
            and_(
                VoteORM.user_id == user_id,
                VoteORM.status.in_(statuses or list(VoteStatusEnum)),
            ),
        )
        rows = (await self._session.scalars(stmt)).all()

        return [VoteEntity(VoteDTO.model_validate(row, from_attributes=True)) for row in rows]

    async def update(self, vote_id: UUID, **kwargs: dict) -> None:
        """Update vote by id."""
        stmt = select(VoteORM).where(VoteORM.id == vote_id)
        vote = await self._session.scalar(stmt)

        if vote:
            for key, value in kwargs.items():
                setattr(vote, key, value)
            await self._session.commit()

    async def delete(self, vote_id: UUID) -> None:
        """Delete vote by id."""
        stmt = select(VoteORM).where(VoteORM.id == vote_id)
        vote = await self._session.scalar(stmt)

        if vote:
            await self._session.delete(vote)
            await self._session.commit()
