from dataclasses import dataclass, field

from reception.domain.exception.room import RoomStatusException
from shared_kernel.domain.entity import Entity
from shared_kernel.domain.value_object import RoomStatus


@dataclass(eq=False, slots=True)
class Room(Entity):
    number: str
    room_status: RoomStatus

    def reserve(self):
        if not self.room_status.is_available:
            raise RoomStatusException

        self.room_status = RoomStatus.RESERVED
