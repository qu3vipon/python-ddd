from dependency_injector import containers, providers

from display.infra.container import DisplayContainer
from reception.infra.container import ReceptionContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "display.presentation.rest.api",
            "reception.presentation.rest.api"
        ]
    )

    display = providers.Container(DisplayContainer)
    reception = providers.Container(ReceptionContainer)
