from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.rooms.exceptions import RoomEntity


class AbstractCreateRoomService(ABC):
    @abstractmethod
    async def process(self, data: UUID) -> RoomEntity: ...
