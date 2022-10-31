from __future__ import annotations

import random
import string
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import ClassVar


@dataclass(slots=True)
class ReservationNumber:
    DATETIME_FORMAT: ClassVar[str] = "%y%m%d%H%M%S"
    RANDOM_STR_LENGTH: ClassVar[int] = 7

    value: str

    @classmethod
    def generate(cls) -> ReservationNumber:
        time_part: str = datetime.utcnow().strftime(cls.DATETIME_FORMAT)
        random_strings: str = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(cls.RANDOM_STR_LENGTH)
        )
        return cls(value=time_part + ":" + random_strings)


class ReservationStatus(str, Enum):
    ONGOING = "ONGOING"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"

    def is_ongoing(self):
        return self == ReservationStatus.ONGOING
