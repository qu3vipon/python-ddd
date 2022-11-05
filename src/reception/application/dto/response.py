from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.value_object.guest import Guest, mobile_type
from shared_kernel.application.dto import BaseResponse
from shared_kernel.domain.value_object import ReservationStatus, RoomStatus


class RoomDTO(BaseModel):
    number: str
    status: RoomStatus

    @classmethod
    def from_entity(cls, room: Room) -> RoomDTO:
        return cls(
            number=room.number,
            status=room.status,
        )


class GuestDTO(BaseModel):
    mobile: mobile_type
    name: Optional[str] = None

    @classmethod
    def from_entity(cls, guest: Guest) -> GuestDTO:
        return cls(
            mobile=guest.mobile,
            name=guest.name,
        )


class ReservationDTO(BaseModel):
    room: RoomDTO
    reservation_number: str
    status: ReservationStatus
    date_in: datetime
    date_out: datetime
    guest: GuestDTO

    @classmethod
    def build_result(cls, reservation: Reservation) -> ReservationDTO:
        return cls(
            room=RoomDTO.from_entity(reservation.room),
            reservation_number=reservation.reservation_number.value,
            status=reservation.status,
            date_in=reservation.date_in,
            date_out=reservation.date_out,
            guest=GuestDTO.from_entity(reservation.guest),
        )


class ReservationResponse(BaseResponse):
    result: ReservationDTO
