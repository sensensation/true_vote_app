from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.votes.enums import VoteStatusEnum


class VoteOutputDTO(BaseModel):
    vote_id: UUID
    room_id: UUID
    user_id: UUID
    option_id: int
    timestamp: datetime
    status: VoteStatusEnum
    blockchain_txn_id: UUID
    timestamp: datetime


class CreateVoteRequestDTO(BaseModel):
    room_id: UUID
    user_id: UUID
    option_id: int
    status: VoteStatusEnum
