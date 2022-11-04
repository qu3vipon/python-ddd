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


class ReservationStatus(ValueObject, str, Enum):
    IN_PROGRESS = "IN-PROGRESS"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"

    def in_progress(self) -> bool:
        return self == ReservationStatus.IN_PROGRESS
