from dataclasses import dataclass, field

from shared_kernel.domain.entity import AggregateRoot
from shared_kernel.domain.value_object import RoomStatus


@dataclass(eq=False, slots=True)
class Room(AggregateRoot):
    number: str
    status: RoomStatus
    image_url: str
    description: str | None = None

    _status: str = field(init=False)
