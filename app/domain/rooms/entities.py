from app.domain.rooms.dto import RoomDTO


class RoomEntity:
    def __init__(self, data: RoomDTO) -> None:
        self.data = data
