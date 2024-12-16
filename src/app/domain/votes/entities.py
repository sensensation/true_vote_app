from app.domain.votes.dto import VoteDTO


class VoteEntity:
    def __init__(self, data: VoteDTO) -> None:
        self.data = data
