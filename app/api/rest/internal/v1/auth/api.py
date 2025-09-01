from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.app_layer.interfaces.api.internal.models.auth import NonceRequestDTO, NonceResponse
from app.containers import Container

router = APIRouter()


@router.post("/nonce")
@inject
async def create_nonce(
    data: NonceRequestDTO,
    service: Annotated[AuthService, Depends(Provide[Container.auth_service])],
) -> NonceResponse:
    return await service.process(NonceResponse(**data.model_dump()))
