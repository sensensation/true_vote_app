from abc import ABC, abstractmethod
from uuid import UUID

from app.app_layer.interfaces.services.votes.dto import VoteOutputDTO


class AbstractVoteService(ABC):
    @abstractmethod
    async def get(self, vote_id: UUID) -> VoteOutputDTO: ...
