from datetime import datetime, timedelta

from reception.domain.exception.check_in import CheckInAuthenticationException, CheckInDateException
from reception.domain.entity.reservation import Reservation
from reception.domain.value_object.guest import mobile_type


class CheckInService:
    _EARLY_CHECK_IN_OFFSET: int = 3
    _LATE_CHECK_IN_OFFSET: int = 6

    @staticmethod
    def _is_valid_date(reservation: Reservation) -> bool:
        return (
            reservation.date_in - timedelta(hours=CheckInService._EARLY_CHECK_IN_OFFSET)
            <= datetime.utcnow()
            <= reservation.date_out - timedelta(hours=CheckInService._LATE_CHECK_IN_OFFSET)
        )

    @staticmethod
    def _is_valid_guest(reservation: Reservation, mobile: mobile_type) -> bool:
        # mobile authentication
        return reservation.guest.mobile == mobile

    def check_in(self, reservation: Reservation, mobile: str) -> None:
        if not self._is_valid_date(reservation=reservation):
            raise CheckInDateException

        if not self._is_valid_guest(reservation=reservation, mobile=mobile):
            raise CheckInAuthenticationException

        reservation.check_in()
