from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.votes.entities import VoteEntity


class AbstractVoteRepository(ABC):
    @abstractmethod
    async def create(self, vote: VoteEntity) -> VoteEntity:
        """Create new vote and return created entity"""
        pass

    @abstractmethod
    async def get_by_user_and_room(self, user_id: UUID, room_id: UUID) -> VoteEntity | None:
        """Get vote by user_id and room_id"""
        pass

    @abstractmethod
    async def get_by_id(self, vote_id: UUID) -> VoteEntity | None:
        """Get vote by id"""
        pass
