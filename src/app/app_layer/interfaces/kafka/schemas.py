from pydantic import BaseModel


class VotesKafkaRequest(BaseModel):
    vote_id: int