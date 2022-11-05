from typing import List

from fastapi import APIRouter, Depends

from display.application.dto.request import GetRoomRequest
from display.application.dto.response import RoomDTO, RoomResponse
from display.application.use_case.query import DisplayQueryUseCase
from display.domain.entity.room import Room

router = APIRouter(prefix="/display")


@router.get("/rooms")
def get_rooms(
    request: GetRoomRequest = Depends(GetRoomRequest),
    display_query: DisplayQueryUseCase = Depends(DisplayQueryUseCase),
):
    rooms: List[Room] = display_query.get_rooms(room_status=request.room_status)
    return RoomResponse(
        detail="ok",
        result=[RoomDTO.from_orm(room) for room in rooms]
    )
