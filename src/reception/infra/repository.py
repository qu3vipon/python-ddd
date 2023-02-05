from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.value_object.reservation import ReservationNumber
from shared_kernel.infra.database.repository import RDBRepository


class ReservationRDBRepository(RDBRepository):
    @staticmethod
    def get_reservation_by_reservation_number(session, reservation_number: ReservationNumber) -> Reservation | None:
        return session.query(Reservation).filter_by(reservation_number=reservation_number).first()

    @staticmethod
    def get_room_by_room_number(session, room_number: str) -> Room | None:
        return session.query(Room).filter_by(number=room_number).first()
