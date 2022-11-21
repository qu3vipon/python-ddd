from fastapi import Depends

from reception.application.exception.reservation import ReservationNotFoundError
from reception.domain.entity.reservation import Reservation
from reception.domain.value_object.reservation import ReservationNumber
from reception.infra.repository import ReservationRDBRepository


class ReservationQueryUseCase:
    def __init__(
        self,
        reservation_repo: ReservationRDBRepository = Depends(ReservationRDBRepository),
    ):
        self.reservation_repo = reservation_repo

    def get_reservation(self, reservation_number: str) -> Reservation:
        reservation_number = ReservationNumber.from_value(reservation_number)

        reservation: Reservation | None = (
            self.reservation_repo.get_reservation_by_reservation_number(reservation_number=reservation_number)
        )
        if not reservation:
            raise ReservationNotFoundError

        return reservation
