from typing import List

from pydantic import BaseModel

from shared_kernel.application.dto import BaseResponse
from shared_kernel.domain.value_object import RoomStatus


class RoomSchema(BaseModel):
    id: int
    number: str
    status: RoomStatus
    image_url: str
    description: str | None

    class Config:
        orm_mode = True


class RoomResponse(BaseResponse):
    result: List[RoomSchema]
