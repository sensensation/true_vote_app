from logging import getLogger
from uuid import uuid4

from app.app_layer.interfaces.services.votes.create_vote.service import AbstractVoteCreateService
from app.app_layer.interfaces.services.votes.get_vote.dto import CreateVoteRequestDTO
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.votes.dto import VoteDTO
from app.domain.votes.entities import VoteEntity
from app.domain.votes.enums import VoteStatusEnum

logger = getLogger(__name__)


class VoteCreateService(AbstractVoteCreateService):
    def __init__(
        self,
        uow: AbcUnitOfWork,
    ) -> None:
        self._uow = uow

    async def process(self, data: CreateVoteRequestDTO) -> VoteEntity:
        """Основной метод создания голоса"""
        await self._validate_room_and_option(data)
        await self._check_existing_vote(data)

        vote_dto = VoteDTO(
            id=uuid4(),
            user_id=data.user_id,
            option_id=data.option_id,
            room_id=data.room_id,
            status=VoteStatusEnum.PENDING,
        )
        vote_entity = VoteEntity(vote_dto)

        async with self._uow:
            created_vote = await self._uow.vote_repo.create(vote_entity)

        logger.info(
            f"Vote {created_vote.data.id} successfully created for user {created_vote.user_id} in room {created_vote.room_id}"
        )

        return created_vote

    async def _validate_room_and_option(self, data: CreateVoteRequestDTO) -> None:
        async with self._uow:
            room = await self._uow.rooms_repo.get(data.room_id)

        if not room:
            raise ValueError(f"Room with id {data.room_id} not found.")

        if data.option_id not in [option.id for option in room.options]:
            raise ValueError(f"Option with id {data.option_id} not found in room {data.room_id}")

    async def _check_existing_vote(self, data: CreateVoteRequestDTO) -> None:
        async with self._uow:
            existing_vote = await self._uow.vote_repo.get_by_user_and_room(data.user_id, data.room_id)

        if existing_vote is not None:
            raise ValueError(f"User {data.user_id} already voted in room {data.room_id}")
