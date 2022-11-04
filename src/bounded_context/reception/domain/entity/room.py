from dataclasses import dataclass, field

from bounded_context.reception.application.exception.room import RoomStatusError
from bounded_context.reception.domain.value_object.room import RoomStatus
from bounded_context.shared_kernel.domain import Entity


@dataclass(eq=False)
class Room(Entity):
    number: str
    status: RoomStatus

    _status: str = field(init=False)

    def reserve(self):
        if not self.status.is_available():
            raise RoomStatusError

        self.status = RoomStatus.RESERVED
