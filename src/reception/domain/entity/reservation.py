from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from reception.application.exception.reservation import ReservationStatusError
from reception.application.exception.room import RoomStatusError
from reception.domain.entity.room import Room
from reception.domain.value_object.guest import Guest
from reception.domain.value_object.reservation import ReservationNumber
from shared_kernel.domain.entity import AggregateRoot
from shared_kernel.domain.value_object import ReservationStatus, RoomStatus


@dataclass(eq=False, slots=True)
class Reservation(AggregateRoot):
    room: Room
    reservation_number: ReservationNumber
    status: ReservationStatus
    date_in: datetime
    date_out: datetime
    guest: Guest

    _number: str = field(init=False)
    _status: str = field(init=False)
    _guest_mobile: str = field(init=False)
    _guest_name: Optional[str] = field(init=False)

    @classmethod
    def make(cls, room: Room, date_in: datetime, date_out: datetime, guest: Guest) -> Reservation:
        room.reserve()
        return cls(
            room=room,
            date_in=date_in,
            date_out=date_out,
            guest=guest,
            reservation_number=ReservationNumber.generate(),
            status=ReservationStatus.IN_PROGRESS,
        )

    def cancel(self):
        if not self.status.in_progress():
            raise ReservationStatusError

        self.status = ReservationStatus.CANCELLED
        self.room.status = RoomStatus.AVAILABLE

    def check_in(self):
        if not self.room.status.is_reserved():
            raise RoomStatusError

        if not self.status.in_progress():
            raise ReservationStatusError

        self.room.status = RoomStatus.OCCUPIED

    def check_out(self):
        if not self.room.status.is_occupied():
            raise RoomStatusError

        if not self.status.in_progress():
            raise ReservationStatusError

        self.status = ReservationStatus.COMPLETE
        self.room.status = RoomStatus.AVAILABLE

    def change_guest(self, guest: Guest):
        self.guest = guest
