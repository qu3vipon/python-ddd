from pydantic import BaseModel

from bounded_context.shared_kernel.value_object import RoomStatus


class GetRoomRequest(BaseModel):
    room_status: RoomStatus
