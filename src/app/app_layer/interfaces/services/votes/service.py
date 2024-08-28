from abc import ABC, abstractmethod
from uuid import UUID

from app.app_layer.interfaces.services.votes.dto import VoteOutputDTO


class AbstractRetrieveVoteService(ABC):
    @abstractmethod
    async def process(self, vote_id: UUID) -> VoteOutputDTO: ...
