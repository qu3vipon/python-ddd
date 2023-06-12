from typing import Callable, ContextManager

from sqlalchemy.orm import Session

from reception.presentation.rest.request import CreateReservationRequest, UpdateGuestRequest
from reception.domain.exception.room import RoomNotFoundException
from reception.application.use_case.query import ReservationQueryUseCase
from reception.domain.entity.reservation import Reservation
from reception.domain.entity.room import Room
from reception.domain.service.check_in import CheckInService
from reception.domain.value_object.guest import Guest, mobile_type
from reception.infra.repository import ReservationRDBRepository


class ReservationCommandUseCase:
    def __init__(
        self,
        reservation_repo: ReservationRDBRepository,
        reservation_query: ReservationQueryUseCase,
        check_in_service: CheckInService,
        db_session: Callable[[], ContextManager[Session]],
    ):
        self.reservation_repo = reservation_repo
        self.reservation_query = reservation_query
        self.check_in_service = check_in_service
        self.db_session = db_session

    def make_reservation(self, request: CreateReservationRequest) -> Reservation:
        with self.db_session() as session:
            room: Room | None = (
                self.reservation_repo.get_room_by_room_number(session=session, room_number=request.room_number)
            )
        if not room:
            raise RoomNotFoundException

        reservation = Reservation.make(
            room=room,
            date_in=request.date_in,
            date_out=request.date_out,
            guest=Guest(mobile=request.guest_mobile, name=request.guest_name)
        )
        with self.db_session() as session:
            self.reservation_repo.add(session=session, instance=reservation)
            self.reservation_repo.commit(session=session)
        return reservation

    def update_guest_info(self, reservation_number: str, request: UpdateGuestRequest) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)

        guest: Guest = Guest(mobile=request.guest_mobile, name=request.guest_name)
        reservation.change_guest(guest=guest)

        with self.db_session() as session:
            self.reservation_repo.add(session=session, instance=reservation)
            self.reservation_repo.commit(session=session)
        return reservation

    def check_in(self, reservation_number: str, mobile: mobile_type) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)
        self.check_in_service.check_in(reservation=reservation, mobile=mobile)

        with self.db_session() as session:
            self.reservation_repo.add(session=session, instance=reservation)
            self.reservation_repo.commit(session=session)
        return reservation

    def check_out(self, reservation_number: str) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)
        reservation.check_out()

        with self.db_session() as session:
            self.reservation_repo.add(session=session, instance=reservation)
            self.reservation_repo.commit(session=session)
        return reservation

    def cancel(self, reservation_number: str) -> Reservation:
        reservation: Reservation = self.reservation_query.get_reservation(reservation_number=reservation_number)
        reservation.cancel()

        with self.db_session() as session:
            self.reservation_repo.add(session=session, instance=reservation)
            self.reservation_repo.commit(session=session)
        return reservation
