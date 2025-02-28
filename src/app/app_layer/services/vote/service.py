from logging import getLogger

from app.app_layer.interfaces.services.votes.dto import CreateVoteRequestDTO, VoteOutputDTO
from app.app_layer.interfaces.services.votes.exceptions import VoteNotFoundException
from app.app_layer.interfaces.services.votes.service import AbstractVoteService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork

logger = getLogger(__name__)


class VoteService(AbstractVoteService):
    def __init__(
        self,
        uow: AbcUnitOfWork,
    ) -> None:
        self._uow = uow

    async def retrieve(self, vote_id: int) -> VoteOutputDTO:
        async with self._uow:
            vote = await self._uow.vote_repo.get(vote_id)

        if not vote:
            raise VoteNotFoundException

        return VoteOutputDTO(
            vote_id=vote.id,
            room_id=vote.id,
            user_id=vote.user_id,
            option_id=vote.option_id,
            status=vote.status,
            blockchain_txn_id=vote.blockchain_txn_id,
            timestamp=vote.timestamp,
            device_type=vote.device_type,
        )

    async def create(self, data: CreateVoteRequestDTO) -> VoteOutputDTO: ...
