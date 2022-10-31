from __future__ import annotations

from enum import Enum


class RoomNumber(str, Enum):
    STD_101 = "Standard 101"
    STD_102 = "Standard 102"
    DLX_201 = "DELUXE 201"
    DLX_202 = "DELUXE 202"


class RoomStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"

    def is_available(self):
        return self == RoomStatus.AVAILABLE
