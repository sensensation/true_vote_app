from abc import ABC, abstractmethod

from app.app_layer.interfaces.services.votes.get_vote.dto import VoteOutputDTO


class AbstractVoteGetService(ABC):
    @abstractmethod
    async def process(self, user_id: int, limit: int) -> list[VoteOutputDTO]: ...
