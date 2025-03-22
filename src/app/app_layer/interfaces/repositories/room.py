from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.rooms.entities import RoomEntity


class AbstractRoomRepository(ABC):
    @abstractmethod
    async def get(self, room_id: UUID) -> RoomEntity | None:
        """Get room by id"""
        pass

    @abstractmethod
    async def create(self, room: RoomEntity) -> None:
        """Create new room"""
        pass

    @abstractmethod
    async def update(self, room: RoomEntity) -> None:
        """Update room"""
        pass
