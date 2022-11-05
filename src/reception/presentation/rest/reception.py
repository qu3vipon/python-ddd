from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from reception.application.dto.request import CheckInRequest, CreateReservationRequest, UpdateGuestRequest
from reception.application.dto.response import ReservationDTO, ReservationResponse
from reception.application.exception.check_in import CheckInAuthenticationError, CheckInDateError
from reception.application.exception.reservation import ReservationNotFoundError, ReservationStatusError
from reception.application.exception.room import RoomNotFoundError, RoomStatusError
from reception.application.use_case.command import ReservationCommandUseCase
from reception.application.use_case.query import ReservationQueryUseCase
from reception.domain.entity.reservation import Reservation
from shared_kernel.application.dto import BaseResponse

router = APIRouter(prefix="/reception")


@router.post(
    "/reservations",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": ReservationResponse},
        status.HTTP_409_CONFLICT: {"model": BaseResponse},
    }
)
def post_reservations(
    create_reservation_request: CreateReservationRequest = Body(),
    reservation_command: ReservationCommandUseCase = Depends(ReservationCommandUseCase),
):
    try:
        reservation: Reservation = reservation_command.make_reservation(request=create_reservation_request)
    except RoomNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except RoomStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ReservationStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationDTO.build_result(reservation=reservation),
    )


@router.get(
    "/reservations/{reservation_number}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ReservationResponse},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponse},
    }
)
def get_reservation(
    reservation_number: str,
    reservation_query: ReservationQueryUseCase = Depends(ReservationQueryUseCase),
):
    try:
        reservation: Reservation = reservation_query.get_reservation(reservation_number=reservation_number)
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationDTO.build_result(reservation=reservation),
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
def patch_reservation(
    reservation_number: str,
    update_quest_request: UpdateGuestRequest = Body(),
    reservation_command: ReservationCommandUseCase = Depends(ReservationCommandUseCase),
):
    try:
        reservation: Reservation = reservation_command.update_guest_info(
            reservation_number=reservation_number, request=update_quest_request
        )
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except RoomStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ReservationStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationDTO.build_result(reservation=reservation),
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
def post_reservation_check_in(
    reservation_number: str,
    check_in_request: CheckInRequest = Body(),
    reservation_command: ReservationCommandUseCase = Depends(ReservationCommandUseCase),
):
    try:
        reservation: Reservation = reservation_command.check_in(
            reservation_number=reservation_number, mobile=check_in_request.mobile
        )
    except CheckInDateError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except CheckInAuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except RoomStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ReservationStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationDTO.build_result(reservation=reservation),
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
def post_reservation_check_out(
    reservation_number: str,
    reservation_command: ReservationCommandUseCase = Depends(ReservationCommandUseCase),
):
    try:
        reservation: Reservation = reservation_command.check_out(reservation_number=reservation_number)
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except RoomStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ReservationStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationDTO.build_result(reservation=reservation),
    )


@router.post("/reservations/{reservation_number}/cancel")
def post_reservation_cancel(
    reservation_number: str,
    reservation_command: ReservationCommandUseCase = Depends(ReservationCommandUseCase),
):
    try:
        reservation: Reservation = reservation_command.cancel(reservation_number=reservation_number)
    except ReservationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except RoomStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ReservationStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return ReservationResponse(
        detail="ok",
        result=ReservationDTO.build_result(reservation=reservation),
    )
