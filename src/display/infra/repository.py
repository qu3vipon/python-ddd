from sqlalchemy.orm import Query, Session

from display.domain.entity.room import Room
from shared_kernel.domain.value_object import RoomStatus
from shared_kernel.infra.database.repository import RDBReadRepository


class RoomRDBRepository(RDBReadRepository):
    @staticmethod
    def get_rooms_by_status(session: Session, room_status: RoomStatus) -> Query:
        return session.query(Room).filter_by(status=room_status)
