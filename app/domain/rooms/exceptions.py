from app.domain.votes.dto import VoteDTO


class RoomEntity:
    def __init__(self, data: VoteDTO) -> None:
        self.data = data
