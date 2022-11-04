from typing import Optional

from fastapi import Depends

from bounded_context.reception.application.exception.reservation import ReservationNotFoundError
from bounded_context.reception.domain.entity.reservation import Reservation
from bounded_context.reception.domain.value_object.reservation import ReservationNumber
from bounded_context.reception.infra.repository.reservation import ReservationRDBRepository


class ReservationQueryUseCase:
    def __init__(
        self,
        reservation_repo: ReservationRDBRepository = Depends(ReservationRDBRepository),
    ):
        self.reservation_repo = reservation_repo

    def get_reservation(self, reservation_number: str) -> Reservation:
        reservation_number = ReservationNumber.from_value(reservation_number)

        reservation: Optional[Reservation] = (
            self.reservation_repo.get_reservation_by_reservation_number(reservation_number=reservation_number)
        )

        if not reservation:
            raise ReservationNotFoundError

        return reservation
