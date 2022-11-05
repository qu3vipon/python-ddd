from fastapi import FastAPI

from display.presentation.rest import display
from reception.presentation.rest import reception
from shared_kernel.infra.database.orm import init_orm_mappers

app = FastAPI(
    title="Python-DDD-Hotel",
    contact={
        "name": "qu3vipon",
        "email": "qu3vipon@gmail.com",
    },
)


@app.get("/")
def health_check():
    return {"ping": "pong"}


app.include_router(reception.router)
app.include_router(display.router)

init_orm_mappers()
