from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app_layer.interfaces.repositories.room import AbstractRoomRepository
from app.domain.rooms.dto import RoomDTO
from app.domain.rooms.entities import RoomEntity
from app.infra.db.models import RoomORM


class RoomRepository(AbstractRoomRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, room_id: UUID) -> RoomEntity | None:
        """Get room by id"""
        stmt = select(RoomORM).where(RoomORM.id == room_id)
        row = await self._session.scalar(stmt)

        if not row:
            return None

        return RoomEntity(RoomDTO.model_validate(row, from_attributes=True))

    async def create(self, room: RoomEntity) -> None:
        """Create new room"""
        db_room = RoomORM(
            id=room.data.id,
            title=room.data.title,
            description=room.data.description,
            start_time=room.data.start_time,
            end_time=room.data.end_time,
            is_closed=room.data.is_closed,
            options=room.data.options,
        )
        self._session.add(db_room)
        await self._session.commit()

    async def update(self, room: RoomEntity) -> None:
        """Update room"""
        db_room = await self._session.query(RoomORM).filter(RoomORM.id == room.data.id).first()

        if not db_room:
            return

        db_room.title = room.data.title
        db_room.description = room.data.description
        db_room.start_time = room.data.start_time
        db_room.end_time = room.data.end_time
        db_room.is_closed = room.data.is_closed
        db_room.options = room.data.options

        await self._session.commit()
