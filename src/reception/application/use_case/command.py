from typing import Optional

from fastapi import Depends

from reception.application.dto.request import CreateReservationRequest, UpdateGuestRequest
from reception.application.exception.room import RoomNotFoundError
from reception.application.use_case.query import ReservationQueryUseCase
from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.service.check_in import CheckInService
from reception.domain.value_object.guest import Guest, mobile_type
from reception.infra.repository import ReservationRDBRepository


class ReservationCommandUseCase:
    def __init__(
        self,
        reservation_repo: ReservationRDBRepository = Depends(ReservationRDBRepository),
        reservation_query: ReservationQueryUseCase = Depends(ReservationQueryUseCase),
        check_in_service: CheckInService = Depends(CheckInService),
    ):
        self.reservation_repo = reservation_repo
        self.reservation_query = reservation_query
        self.check_in_service = check_in_service

    def make_reservation(self, request: CreateReservationRequest) -> Reservation:
        room: Optional[Room] = (
            self.reservation_repo.get_room_by_room_number(room_number=request.room_number)
        )
        if not room:
            raise RoomNotFoundError

        reservation = Reservation.make(
            room=room,
            date_in=request.date_in,
            date_out=request.date_out,
            guest=Guest(mobile=request.guest_mobile, name=request.guest_name)
        )
        self.reservation_repo.add(reservation)
        self.reservation_repo.commit()
        self.reservation_repo.refresh(reservation)
        return reservation

    def update_guest_info(self, reservation_number: str, request: UpdateGuestRequest) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)

        guest: Guest = Guest(mobile=request.guest_mobile, name=request.guest_name)
        reservation.change_guest(guest=guest)

        self.reservation_repo.add(reservation)
        self.reservation_repo.commit()
        self.reservation_repo.refresh(reservation)
        return reservation

    def check_in(self, reservation_number: str, mobile: mobile_type) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)

        self.check_in_service.check_in(reservation=reservation, mobile=mobile)

        self.reservation_repo.add(reservation)
        self.reservation_repo.commit()
        self.reservation_repo.refresh(reservation)
        return reservation

    def check_out(self, reservation_number: str) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)

        reservation.check_out()

        self.reservation_repo.add(reservation)
        self.reservation_repo.commit()
        self.reservation_repo.refresh(reservation)
        return reservation

    def cancel(self, reservation_number: str) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)

        reservation.cancel()

        self.reservation_repo.add(reservation)
        self.reservation_repo.commit()
        self.reservation_repo.refresh(reservation)
        return reservation
