from logging import getLogger
from uuid import UUID

from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.app_layer.interfaces.services.votes.dto import VoteOutputDTO
from app.app_layer.interfaces.services.votes.service import AbstractRetrieveVoteService


logger = getLogger(__name__)


class RetrieveVoteService(AbstractRetrieveVoteService):
    def __init__(
        self,
        uow: AbcUnitOfWork,
    ) -> None:
        self._uow = uow

    async def process(self, vote_id: UUID) -> VoteOutputDTO:
        pass
