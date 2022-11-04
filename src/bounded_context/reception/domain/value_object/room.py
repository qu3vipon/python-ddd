from __future__ import annotations

from enum import Enum

from bounded_context.shared_kernel.domain import ValueObject


class RoomStatus(ValueObject, str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"

    def is_available(self) -> bool:
        return self == RoomStatus.AVAILABLE

    def is_occupied(self) -> bool:
        return self == RoomStatus.OCCUPIED
