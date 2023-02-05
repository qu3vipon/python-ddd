from dependency_injector import containers, providers

from reception.application.use_case.command import ReservationCommandUseCase
from reception.application.use_case.query import ReservationQueryUseCase
from reception.domain.service.check_in import CheckInService
from reception.infra.repository import ReservationRDBRepository
from shared_kernel.infra.database.connection import get_db_session


class ReceptionContainer(containers.DeclarativeContainer):
    reservation_repo = providers.Factory(ReservationRDBRepository)

    check_in_service = providers.Factory(CheckInService)

    reservation_query = providers.Factory(
        ReservationQueryUseCase,
        reservation_repo=reservation_repo,
        db_session=get_db_session,
    )
    reservation_command = providers.Factory(
        ReservationCommandUseCase,
        reservation_repo=reservation_repo,
        reservation_query=reservation_query,
        check_in_service=check_in_service,
        db_session=get_db_session,
    )
