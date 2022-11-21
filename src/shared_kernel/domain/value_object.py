from enum import Enum, EnumMeta
from typing import Any, TypeVar

ValueObjectType = TypeVar("ValueObjectType", bound="ValueObject")


class ValueObject:
    def __composite_values__(self):
        return self.value,

    @classmethod
    def from_value(cls, value: Any) -> ValueObjectType | None:
        if isinstance(cls, EnumMeta):
            for item in cls:
                if item.value == value:
                    return item
            return None
        else:
            return cls(value=value)


class RoomStatus(ValueObject, str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"

    def is_available(self) -> bool:
        return self == RoomStatus.AVAILABLE

    def is_reserved(self) -> bool:
        return self == RoomStatus.RESERVED

    def is_occupied(self) -> bool:
        return self == RoomStatus.OCCUPIED


class ReservationStatus(ValueObject, str, Enum):
    IN_PROGRESS = "IN-PROGRESS"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"

    def in_progress(self) -> bool:
        return self == ReservationStatus.IN_PROGRESS
