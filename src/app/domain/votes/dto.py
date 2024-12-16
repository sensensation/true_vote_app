from typing import Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.domain.votes.enums import VoteStatusEnum


class VoteDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    option_id: int
    device_type: str
    status: VoteStatusEnum
    meta: Any
    blockchain_txn_id: UUID
