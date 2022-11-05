from dataclasses import dataclass, field
from typing import Optional

from bounded_context.shared_kernel.domain import AggregateRoot
from bounded_context.shared_kernel.value_object import RoomStatus


@dataclass(eq=False, slots=True)
class Room(AggregateRoot):
    number: str
    status: RoomStatus
    image_url: str
    description: Optional[str] = None

    _status: str = field(init=False)
