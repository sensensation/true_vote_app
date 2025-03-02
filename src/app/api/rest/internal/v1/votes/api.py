from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.rest.internal.v1.errors import VOTE_WAS_NOT_FOUND_ERROR
from app.app_layer.interfaces.services.votes.get_vote.dto import CreateVoteRequestDTO, VoteOutputDTO
from app.app_layer.interfaces.services.votes.get_vote.exceptions import VoteNotFoundException
from app.app_layer.services.votes.create_vote.service import VoteCreateService
from app.app_layer.services.votes.get_vote.serivce import VoteGetService
from app.containers import Container

router = APIRouter()


@router.get("/{user_id}/retrieve")
@inject
async def retrieve_votes_v1(
    user_id: UUID,
    limit: int = 10,
    service: VoteGetService = Depends(Provide[Container.vote_get_service]),
) -> list[VoteOutputDTO]:
    try:
        return await service.process(user_id, limit)
    except VoteNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=VOTE_WAS_NOT_FOUND_ERROR)


@router.post("/create")
@inject
async def create_vote_v1(
    data: CreateVoteRequestDTO,
    service: VoteCreateService = Depends(Provide[Container.vote_create_service]),
) -> VoteOutputDTO:
    try:
        vote = await service.create(CreateVoteRequestDTO)
    except Exception:
        pass
    return vote
