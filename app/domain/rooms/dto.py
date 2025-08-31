from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class RoomDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    is_closed: bool = False
    blockchain_room_address: str | None = None

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, end_time: datetime, info: dict[str, Any]) -> datetime:
        """Проверяет, что время завершения не раньше времени начала."""
        start_time = info.data.get("start_time")
        if start_time and end_time < start_time:
            msg = "Время завершения голосования не может быть раньше времени начала"
            raise ValueError(msg)
        return end_time
