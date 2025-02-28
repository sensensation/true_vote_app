from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.rest.internal.v1.errors import VOTE_WAS_NOT_FOUND_ERROR
from app.app_layer.interfaces.services.votes.dto import CreateVoteRequestDTO, VoteOutputDTO
from app.app_layer.interfaces.services.votes.exceptions import VoteNotFoundException
from app.app_layer.services.vote.service import VoteService
from app.containers import Container

router = APIRouter()


@router.get("/{vote_id}/retrieve")
@inject
async def retrieve_vote_v1(
    vote_id: UUID,
    service: VoteService = Depends(Provide[Container.vote_service]),
) -> VoteOutputDTO:
    try:
        return await service.retrieve(vote_id)
    except VoteNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=VOTE_WAS_NOT_FOUND_ERROR)


@router.post("/create")
@inject
async def create_vote_v1(
    data: CreateVoteRequestDTO,
    service: VoteService = Depends(Provide[Container.vote_service]),
) -> VoteOutputDTO:
    try:
        vote = await service.create(CreateVoteRequestDTO)
    except Exception:
        pass
    return vote
