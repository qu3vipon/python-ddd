from typing import List

from fastapi import APIRouter, Depends

from bounded_context.display.application.dto.request import GetRoomRequest
from bounded_context.display.application.dto.response import RoomResponse, RoomDTO
from bounded_context.display.application.use_case.query import DisplayQueryUseCase
from bounded_context.display.domain.entity.room import Room

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
