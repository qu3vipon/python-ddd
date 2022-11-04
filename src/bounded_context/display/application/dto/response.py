from typing import List

from pydantic import BaseModel

from bounded_context.shared_kernel.dto import BaseResponse
from bounded_context.shared_kernel.value_object import RoomStatus


class RoomDTO(BaseModel):
    id: int
    number: str
    status: RoomStatus
    image_url: str
    description: str | None

    class Config:
        orm_mode = True


class RoomResponse(BaseResponse):
    result: List[RoomDTO]
