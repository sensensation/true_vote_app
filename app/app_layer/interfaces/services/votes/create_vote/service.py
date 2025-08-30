from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.votes.entities import VoteEntity


class AbstractVoteCreateService(ABC):
    @abstractmethod
    async def process(self, vote_id: UUID) -> VoteEntity: ...
