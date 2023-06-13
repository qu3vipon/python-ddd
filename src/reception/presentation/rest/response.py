from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.value_object.guest import Guest, mobile_type
from shared_kernel.presentation.response import BaseResponse
from shared_kernel.domain.value_object import ReservationStatus, RoomStatus


class RoomSchema(BaseModel):
    number: str
    status: RoomStatus

    @classmethod
    def from_entity(cls, room: Room) -> RoomSchema:
        return cls(
            number=room.number,
            status=room.room_status,
        )


class GuestSchema(BaseModel):
    mobile: mobile_type
    name: str | None = None

    @classmethod
    def from_entity(cls, guest: Guest) -> GuestSchema:
        return cls(
            mobile=guest.mobile,
            name=guest.name,
        )


class ReservationSchema(BaseModel):
    room: RoomSchema
    reservation_number: str
    status: ReservationStatus
    date_in: datetime
    date_out: datetime
    guest: GuestSchema

    @classmethod
    def build(cls, reservation: Reservation) -> ReservationSchema:
        return cls(
            room=RoomSchema.from_entity(reservation.room),
            reservation_number=reservation.reservation_number.value,
            status=reservation.reservation_status.value,
            date_in=reservation.date_in,
            date_out=reservation.date_out,
            guest=GuestSchema.from_entity(reservation.guest),
        )


class ReservationResponse(BaseResponse):
    result: ReservationSchema
