from enum import Enum, EnumMeta
from typing import Any, TypeVar

from shared_kernel.domain.exception import ValueObjectValidationError

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
            try:
                instance = cls(value=value)
                instance.__validate__()
                return instance
            except Exception:
                raise ValueObjectValidationError

    def __validate__(self) -> None:
        raise NotImplementedError


class RoomStatus(ValueObject, str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"

    @property
    def is_available(self) -> bool:
        return self == RoomStatus.AVAILABLE

    @property
    def is_reserved(self) -> bool:
        return self == RoomStatus.RESERVED

    @property
    def is_occupied(self) -> bool:
        return self == RoomStatus.OCCUPIED


class ReservationStatus(ValueObject, str, Enum):
    IN_PROGRESS = "IN-PROGRESS"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"

    @property
    def in_progress(self) -> bool:
        return self == ReservationStatus.IN_PROGRESS
