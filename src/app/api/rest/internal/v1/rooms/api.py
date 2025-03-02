from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.app_layer.interfaces.services.rooms.create_room.dto import CreateRoomRequest
from app.containers import Container

router = APIRouter()


@router.post("/rooms/create")
@inject
async def create_room(
    data: CreateRoomRequest,
    service: RoomService = Depends(Provide[Container.room_create_service]),
) -> RoomOutputDTO:
    room = await service.process(data)
    return room


@router.post("/rooms/{room_uuid}/options/create")
async def create_options_for_room(room_uuid: UUID, data: CreateOptionRequest, service: RoomService = Depends(...)):
    # service.create_option(room_uuid, data)
    ...
