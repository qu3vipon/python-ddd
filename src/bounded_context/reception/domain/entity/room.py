from dataclasses import dataclass, field

from bounded_context.reception.application.exception.room import RoomStatusError
from bounded_context.shared_kernel.domain import Entity
from bounded_context.shared_kernel.value_object import RoomStatus


@dataclass(eq=False, slots=True)
class Room(Entity):
    number: str
    status: RoomStatus

    _status: str = field(init=False)

    def reserve(self):
        if not self.status.is_available():
            raise RoomStatusError

        self.status = RoomStatus.RESERVED
