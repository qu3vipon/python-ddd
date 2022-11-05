from dataclasses import dataclass, field

from reception.application.exception.room import RoomStatusError
from shared_kernel.domain.entity import Entity
from shared_kernel.domain.value_object import RoomStatus


@dataclass(eq=False, slots=True)
class Room(Entity):
    number: str
    status: RoomStatus

    _status: str = field(init=False)

    def reserve(self):
        if not self.status.is_available():
            raise RoomStatusError

        self.status = RoomStatus.RESERVED
