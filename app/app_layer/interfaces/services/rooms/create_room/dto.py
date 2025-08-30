from datetime import datetime

from pydantic import BaseModel


class CreateRoomRequest(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    is_closed: bool = False
