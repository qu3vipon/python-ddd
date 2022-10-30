from __future__ import annotations

import random
import string
from datetime import datetime
from enum import Enum

from context.shared_kernel.domain import FactoryOnly


class ReservationNumber(FactoryOnly):
    DATETIME_FORMAT: str = "%y%m%d%H%M%S"
    RANDOM_STR_LENGTH: int = 7

    def __init__(self, value: str, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    @classmethod
    def generate(cls) -> ReservationNumber:
        time_part: str = datetime.utcnow().strftime(cls.DATETIME_FORMAT)
        random_strings: str = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(cls.RANDOM_STR_LENGTH)
        )
        return cls(value=time_part + ":" + random_strings, direct=False)


class ReservationStatus(str, Enum):
    ONGOING = "ONGOING"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"

    def is_ongoing(self):
        return self == ReservationStatus.ONGOING
