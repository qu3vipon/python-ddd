from typing import Optional

from bounded_context.reception.domain.entity.reservation import Reservation
from bounded_context.reception.domain.entity.room import Room
from bounded_context.reception.domain.value_object.reservation import ReservationNumber
from ddd_hotel.database.repository import RDBRepository


class ReservationRDBRepository(RDBRepository):
    def get_reservation_by_reservation_number(self, reservation_number: ReservationNumber) -> Optional[Reservation]:
        return self.session.query(Reservation).filter_by(reservation_number=reservation_number).first()

    def get_room_by_room_number(self, room_number: str) -> Optional[Room]:
        return self.session.query(Room).filter_by(number=room_number).first()
