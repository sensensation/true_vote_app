from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.rest.internal.v1.errors import VOTE_WAS_NOT_FOUND_ERROR
from app.app_layer.interfaces.services.votes.get_vote.dto import CreateVoteRequestDTO, VoteOutputDTO
from app.app_layer.interfaces.services.votes.get_vote.exceptions import VoteNotFoundError
from app.app_layer.services.votes.create_vote.service import VoteCreateService
from app.app_layer.services.votes.get_vote.serivce import VoteGetService
from app.containers import Container

router = APIRouter()


@router.get("/{user_id}/retrieve")
@inject
async def retrieve_votes_v1(
    service: Annotated[VoteGetService, Depends(Provide[Container.vote_get_service])],
    user_id: UUID,
    limit: int = 10,
) -> list[VoteOutputDTO]:
    try:
        return await service.process(user_id, limit)
    except VoteNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=VOTE_WAS_NOT_FOUND_ERROR) from e


@router.post("/create")
@inject
async def create_vote_v1(
    data: CreateVoteRequestDTO,
    service: Annotated[VoteCreateService, Depends(Provide[Container.vote_create_service])],
) -> VoteOutputDTO:
    return await service.process(CreateVoteRequestDTO(**data.model_dump()))
