from logging import getLogger

from app.app_layer.interfaces.services.votes.create_vote.service import AbstractVoteCreateService
from app.app_layer.interfaces.services.votes.get_vote.dto import VoteOutputDTO
from app.app_layer.interfaces.services.votes.get_vote.exceptions import VoteNotFoundException
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.votes.entities import VoteEntity

logger = getLogger(__name__)


class VoteCreateService(AbstractVoteCreateService):
    def __init__(
        self,
        uow: AbcUnitOfWork,
    ) -> None:
        self._uow = uow

    async def process(self, vote_id: int) -> VoteEntity: ...
