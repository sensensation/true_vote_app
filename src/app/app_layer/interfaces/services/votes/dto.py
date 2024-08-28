from uuid import UUID

from pydantic import BaseModel


class VoteOutputDTO(BaseModel):
    vote_id: UUID
