from logging import getLogger

from app.app_layer.interfaces.services.votes.get_vote.dto import VoteOutputDTO
from app.app_layer.interfaces.services.votes.get_vote.exceptions import VoteNotFoundError
from app.app_layer.interfaces.services.votes.get_vote.service import AbstractVoteGetService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork

logger = getLogger(__name__)


class VoteGetService(AbstractVoteGetService):
    def __init__(
        self,
        uow: AbcUnitOfWork,
    ) -> None:
        self._uow = uow

    async def process(self, user_id: int, limit: int) -> list[VoteOutputDTO]:
        async with self._uow:
            votes = await self._uow.vote_repo.get_list_by_user(user_id, limit)

        if not votes:
            raise VoteNotFoundError

        return [
            VoteOutputDTO(
                vote_id=vote.id,
                room_id=vote.room_id,
                user_id=vote.user_id,
                option_id=vote.option_id,
                status=vote.status,
                blockchain_txn_id=vote.blockchain_txn_id,
                timestamp=vote.timestamp,
            )
            for vote in votes
        ]
