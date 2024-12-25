from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.app_layer.interfaces.services.votes.dto import VoteOutputDTO
from app.app_layer.services.vote_retrieve.service import RetrieveVoteService
from app.containers import Container

router = APIRouter()


@router.get("/{vote_id}/retrieve")
@inject
async def retrieve_vote_v1(
    vote_id: UUID,
    service: RetrieveVoteService = Depends(Provide[Container.retrieve_vote_service]),
) -> VoteOutputDTO:
    pass
