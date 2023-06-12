from fastapi import FastAPI

from display.presentation.rest import api as display_api
from reception.presentation.rest import api as reception_api
from shared_kernel.infra.container import AppContainer
from shared_kernel.infra.database.orm import init_orm_mappers

app_container = AppContainer()

app = FastAPI(
    title="Python-DDD-Hotel",
    contact={
        "name": "qu3vipon",
        "email": "qu3vipon@gmail.com",
    },
)

app.container = app_container
app.include_router(reception_api.router)
app.include_router(display_api.router)

init_orm_mappers()


@app.get("/")
def health_check():
    return {"ping": "pong"}
