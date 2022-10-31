from dataclasses import dataclass

from bounded_context.reception.application.exception.room import RoomStatusError
from bounded_context.reception.domain.value_object.room import RoomNumber, RoomStatus
from bounded_context.shared_kernel.domain import Entity


@dataclass(eq=False, slots=True)
class Room(Entity):
    number: RoomNumber
    status: RoomStatus

    def reserve(self):
        if not self.status.is_available:
            raise RoomStatusError

        self.status = RoomStatus.RESERVED
