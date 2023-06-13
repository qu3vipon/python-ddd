from typing import Callable, ContextManager

from sqlalchemy.orm import Session

from reception.domain.entity.room import Room
from reception.domain.exception.reservation import ReservationNotFoundException
from reception.domain.entity.reservation import Reservation
from reception.domain.exception.room import RoomNotFoundException
from reception.domain.value_object.reservation import ReservationNumber
from reception.infra.repository import ReservationRDBRepository


class ReservationQueryUseCase:
    def __init__(
        self,
        reservation_repo: ReservationRDBRepository,
        db_session: Callable[[], ContextManager[Session]],
    ):
        self.reservation_repo = reservation_repo
        self.db_session = db_session

    def get_room(self, room_number: str) -> Room:
        with self.db_session() as session:
            room: Room | None = (
                self.reservation_repo.get_room_by_room_number(session=session, room_number=room_number)
            )
        if not room:
            raise RoomNotFoundException
        return room

    def get_reservation(self, reservation_number: str) -> Reservation:
        reservation_number = ReservationNumber.from_value(value=reservation_number)

        with self.db_session() as session:
            reservation: Reservation | None = (
                self.reservation_repo.get_reservation_by_reservation_number(
                    session=session, reservation_number=reservation_number
                )
            )

        if not reservation:
            raise ReservationNotFoundException
        return reservation
