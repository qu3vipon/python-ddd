from typing import List

from fastapi import Depends
from sqlalchemy.orm import Query

from bounded_context.display.domain.entity.room import Room
from bounded_context.display.infra.repository import RoomRDBRepository
from bounded_context.shared_kernel.value_object import RoomStatus


class DisplayQueryUseCase:
    def __init__(
        self,
        room_repo: RoomRDBRepository = Depends(RoomRDBRepository),
    ):
        self.room_repo = room_repo

    def get_rooms(self, room_status: RoomStatus) -> List[Room]:
        room_status: RoomStatus = RoomStatus.from_value(room_status)

        rooms: Query = self.room_repo.get_rooms_by_status(room_status=room_status)
        return list(rooms)
