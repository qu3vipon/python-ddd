from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from bounded_context.reception.application.exception.reservation import ReservationStatusError
from bounded_context.reception.domain.entity.room import Room
from bounded_context.reception.domain.value_object.guest import Guest
from bounded_context.reception.domain.value_object.reservation import ReservationNumber, ReservationStatus
from bounded_context.reception.domain.value_object.room import RoomStatus
from bounded_context.shared_kernel.domain import AggregateRoot


@dataclass(eq=False, slots=True)
class Reservation(AggregateRoot):
    room: Room
    reservation_number: ReservationNumber
    status: ReservationStatus
    date_in: datetime
    date_out: datetime
    guest: Guest

    @classmethod
    def make(cls, room: Room, date_in: datetime, date_out: datetime, guest: Guest) -> Reservation:
        room.reserve()
        return cls(
            room=room,
            date_in=date_in,
            date_out=date_out,
            guest=guest,
            reservation_number=ReservationNumber.generate(),
            status=ReservationStatus.ONGOING,
        )

    def cancel(self):
        if not self.status.is_ongoing():
            raise ReservationStatusError

        self.status = ReservationStatus.CANCELLED

    def check_in(self):
        if not self.status.is_ongoing():
            raise ReservationStatusError

        self.room.status = RoomStatus.OCCUPIED

    def check_out(self):
        if not self.status.is_ongoing():
            raise ReservationStatusError

        self.status = ReservationStatus.COMPLETE
        self.room.status = RoomStatus.AVAILABLE

    def change_guest(self, guest: Guest):
        self.guest = guest
