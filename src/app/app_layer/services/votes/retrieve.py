from logging import getLogger

from app.app_layer.interfaces.services.votes.dto import VoteOutputDTO
from app.app_layer.interfaces.services.votes.service import AbstractRetrieveVoteService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork


logger = getLogger(__name__)


class RetrieveVoteService(AbstractRetrieveVoteService):
    def __init__(
        self,
        uow: AbcUnitOfWork,
    ) -> None:
        self._uow = uow

    async def process(self, vote_id: int) -> VoteOutputDTO:
        async with self._uow:
            vote = await self._uow.vote_repo.get(vote_id)

        return VoteOutputDTO(
            vote_id=vote.id,
            user_id=vote.user_id,
            option_id=vote.option_id,
            status=vote.status,
            blockchain_txn_id=vote.blockchain_txn_id,
        )