from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from reception.application.use_case.command import ReservationCommandUseCase
from reception.application.use_case.query import ReservationQueryUseCase
from reception.domain.exception.check_in import CheckInAuthenticationException, CheckInDateException
from reception.domain.exception.reservation import ReservationNotFoundException, ReservationStatusException
from reception.domain.exception.room import RoomNotFoundException, RoomStatusException
from reception.domain.entity.reservation import Reservation
from reception.presentation.rest.request import CheckInRequest, CreateReservationRequest, UpdateGuestRequest
from reception.presentation.rest.response import ReservationSchema, ReservationResponse
from shared_kernel.presentation.response import BaseResponse
from shared_kernel.infra.container import AppContainer

router = APIRouter(prefix="/reception")


@router.post(
    "/reservations",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": ReservationResponse},
        status.HTTP_409_CONFLICT: {"model": BaseResponse},
    }
)
@inject
def post_reservations(
    create_reservation_request: CreateReservationRequest = Body(),
    reservation_command: ReservationCommandUseCase = Depends(Provide[AppContainer.reception.reservation_command]),
) -> ReservationResponse:
    try:
        reservation: Reservation = reservation_command.make_reservation(request=create_reservation_request)
    except RoomNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except (RoomStatusException, ReservationStatusException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationSchema.build(reservation=reservation),
    )


@router.get(
    "/reservations/{reservation_number}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ReservationResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponse},
    }
)
@inject
def get_reservation(
    reservation_number: str,
    reservation_query: ReservationQueryUseCase = Depends(Provide[AppContainer.reception.reservation_query]),
) -> ReservationResponse:
    try:
        reservation: Reservation = reservation_query.get_reservation(reservation_number=reservation_number)
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationSchema.build(reservation=reservation),
    )


@router.patch(
    "/reservations/{reservation_number}/guest",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ReservationResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponse},
        status.HTTP_409_CONFLICT: {"model": BaseResponse},
    }
)
@inject
def patch_reservation(
    reservation_number: str,
    update_quest_request: UpdateGuestRequest = Body(),
    reservation_command: ReservationCommandUseCase = Depends(Provide[AppContainer.reception.reservation_command]),
) -> ReservationResponse:
    try:
        reservation: Reservation = reservation_command.update_guest_info(
            reservation_number=reservation_number, request=update_quest_request
        )
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except (RoomStatusException, ReservationStatusException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationSchema.build(reservation=reservation),
    )


@router.post(
    "/reservations/{reservation_number}/check-in",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ReservationResponse},
        status.HTTP_400_BAD_REQUEST: {"model": BaseResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponse},
        status.HTTP_409_CONFLICT: {"model": BaseResponse},
    }
)
@inject
def post_reservation_check_in(
    reservation_number: str,
    check_in_request: CheckInRequest = Body(),
    reservation_command: ReservationCommandUseCase = Depends(Provide[AppContainer.reception.reservation_command]),
) -> ReservationResponse:
    try:
        reservation: Reservation = reservation_command.check_in(
            reservation_number=reservation_number, mobile=check_in_request.mobile
        )
    except (CheckInDateException, CheckInAuthenticationException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except (RoomStatusException, ReservationStatusException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationSchema.build(reservation=reservation),
    )


@router.post(
    "/reservations/{reservation_number}/check-out",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ReservationResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponse},
        status.HTTP_409_CONFLICT: {"model": BaseResponse},
    }
)
@inject
def post_reservation_check_out(
    reservation_number: str,
    reservation_command: ReservationCommandUseCase = Depends(Provide[AppContainer.reception.reservation_command]),
) -> ReservationResponse:
    try:
        reservation: Reservation = reservation_command.check_out(reservation_number=reservation_number)
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except (RoomStatusException, ReservationStatusException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationSchema.build(reservation=reservation),
    )


@router.post("/reservations/{reservation_number}/cancel")
@inject
def post_reservation_cancel(
    reservation_number: str,
    reservation_command: ReservationCommandUseCase = Depends(Provide[AppContainer.reception.reservation_command]),
) -> ReservationResponse:
    try:
        reservation: Reservation = reservation_command.cancel(reservation_number=reservation_number)
    except ReservationNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except (RoomStatusException, ReservationStatusException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationSchema.build(reservation=reservation),
    )
