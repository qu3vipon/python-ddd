from dependency_injector import containers, providers

from display.application.use_case.query import DisplayQueryUseCase
from display.infra.repository import RoomRDBRepository
from shared_kernel.infra.database.connection import get_db_session


class DisplayContainer(containers.DeclarativeContainer):
    room_repo = providers.Factory(RoomRDBRepository)

    query = providers.Factory(
        DisplayQueryUseCase,
        room_repo=room_repo,
        db_session=get_db_session,
    )
