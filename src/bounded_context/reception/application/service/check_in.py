from datetime import timedelta, datetime

from bounded_context.reception.application.exception.check_in import CheckInAuthenticationError, CheckInDateError
from bounded_context.reception.domain.entity.reservation import Reservation


class CheckInService:
    EARLY_CHECK_IN_OFFSET: int = 3
    LATE_CHECK_IN_OFFSET: int = 6

    @staticmethod
    def _is_valid_date(reservation: Reservation) -> bool:
        return (
            reservation.date_in - timedelta(hours=CheckInService.EARLY_CHECK_IN_OFFSET)
            <= datetime.now()
            <= reservation.date_out - timedelta(hours=CheckInService.LATE_CHECK_IN_OFFSET)
        )

    @staticmethod
    def _is_valid_guest(reservation: Reservation, mobile: str) -> bool:
        return reservation.guest.mobile == mobile

    def check_in(self, reservation: Reservation, mobile: str) -> None:
        if not self._is_valid_date(reservation=reservation):
            raise CheckInDateError

        if not self._is_valid_guest(reservation=reservation, mobile=mobile):
            raise CheckInAuthenticationError

        reservation.check_in()
