from pydantic import BaseModel

from shared_kernel.domain.value_object import RoomStatus


class GetRoomRequest(BaseModel):
    status: RoomStatus
