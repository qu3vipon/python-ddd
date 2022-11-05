from sqlalchemy.orm import Query

from display.domain.entity.room import Room
from shared_kernel.domain.value_object import RoomStatus
from shared_kernel.infra.database.repository import RDBReadRepository


class RoomRDBRepository(RDBReadRepository):
    def get_rooms_by_status(self, room_status: RoomStatus) -> Query:
        return self.session.query(Room).filter_by(status=room_status)
