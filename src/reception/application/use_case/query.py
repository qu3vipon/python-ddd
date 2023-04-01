from typing import Callable, ContextManager

from sqlalchemy.orm import Session

from reception.domain.exception.reservation import ReservationNotFoundException
from reception.domain.entity.reservation import Reservation
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

    def get_reservation(self, reservation_number: str) -> Reservation:
        reservation_number = ReservationNumber.from_value(reservation_number)

        with self.db_session() as session:
            reservation: Reservation | None = (
                self.reservation_repo.get_reservation_by_reservation_number(
                    session=session, reservation_number=reservation_number
                )
            )

        if not reservation:
            raise ReservationNotFoundException

        return reservation
