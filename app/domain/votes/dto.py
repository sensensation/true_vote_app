from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.votes.enums import VoteStatusEnum


class VoteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    option_id: int
    room_id: int
    status: VoteStatusEnum
    meta: dict[str, Any] = {}
    blockchain_txn_id: UUID | None = None
