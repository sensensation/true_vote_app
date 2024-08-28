from logging import getLogger
from uuid import UUID

from app.app_layer.interfaces.services.vote.dto import VoteOutputDTO
from app.app_layer.interfaces.services.vote.service import AbstractRetrieveVoteService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork


logger = getLogger(__name__)


class RetrieveVoteService(AbstractRetrieveVoteService):
    def __init__(
        self,
        uow: AbcUnitOfWork,
    ) -> None:
        self._uow = uow

    async def process(self, vote_id: UUID) -> VoteOutputDTO: ...
