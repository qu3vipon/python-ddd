from dataclasses import dataclass

from bounded_context.shared_kernel.domain import AggregateRoot
from bounded_context.shared_kernel.value_object import RoomStatus


@dataclass(eq=False)
class Room(AggregateRoot):
    number: str
    status: RoomStatus
    image_url: str
    description: str
