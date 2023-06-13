from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from reception.domain.exception.reservation import ReservationStatusException
from reception.domain.exception.room import RoomStatusException
from reception.domain.entity.room import Room
from reception.domain.value_object.guest import Guest
from reception.domain.value_object.reservation import ReservationNumber
from shared_kernel.domain.entity import AggregateRoot
from shared_kernel.domain.value_object import ReservationStatus, RoomStatus


@dataclass(eq=False, slots=True)
class Reservation(AggregateRoot):
    room: Room
    reservation_number: ReservationNumber
    reservation_status: ReservationStatus
    date_in: datetime
    date_out: datetime
    guest: Guest

    @classmethod
    def make(
        cls, room: Room, date_in: datetime, date_out: datetime, guest: Guest
    ) -> Reservation:
        room.reserve()
        return cls(
            room=room,
            date_in=date_in,
            date_out=date_out,
            guest=guest,
            reservation_number=ReservationNumber.generate(),
            reservation_status=ReservationStatus.IN_PROGRESS,
        )

    def cancel(self):
        if not self.reservation_status.in_progress:
            raise ReservationStatusException

        self.reservation_status = ReservationStatus.CANCELLED
        self.room.room_status = RoomStatus.AVAILABLE

    def check_in(self):
        if not self.room.room_status.is_reserved:
            raise RoomStatusException

        if not self.reservation_status.in_progress:
            raise ReservationStatusException

        self.room.room_status = RoomStatus.OCCUPIED

    def check_out(self):
        if not self.room.room_status.is_occupied:
            raise RoomStatusException

        if not self.reservation_status.in_progress:
            raise ReservationStatusException

        self.reservation_status = ReservationStatus.COMPLETE
        self.room.room_status = RoomStatus.AVAILABLE

    def change_guest(self, guest: Guest):
        self.guest = guest
