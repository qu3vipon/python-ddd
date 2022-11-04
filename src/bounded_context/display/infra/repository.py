from sqlalchemy.orm import Query

from bounded_context.display.domain.entity.room import Room
from bounded_context.shared_kernel.value_object import RoomStatus
from ddd_hotel.database.repository import RDBReadRepository


class RoomRDBRepository(RDBReadRepository):
    def get_rooms_by_status(self, room_status: RoomStatus) -> Query:
        return self.session.query(Room).filter_by(status=room_status)
