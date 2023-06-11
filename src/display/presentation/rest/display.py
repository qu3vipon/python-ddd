from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from display.presentation.rest.schema.request import GetRoomRequest
from display.presentation.rest.schema.response import RoomSchema, RoomResponse
from display.application.use_case.query import DisplayQueryUseCase
from display.domain.entity.room import Room
from shared_kernel.infra.container import AppContainer

router = APIRouter(prefix="/display")


@router.get("/rooms")
@inject
def get_rooms(
    request: GetRoomRequest = Depends(),
    display_query: DisplayQueryUseCase = Depends(Provide[AppContainer.display.query]),
) -> RoomResponse:
    rooms: List[Room] = display_query.get_rooms(room_status=request.status)
    return RoomResponse(
        detail="ok",
        result=[RoomSchema.from_orm(room) for room in rooms]
    )
