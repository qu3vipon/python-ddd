from fastapi import FastAPI

from presentation.rest import base

app = FastAPI(
    title="Python-DDD",
    contact={
        "name": "qu3vipon",
        "email": "qu3vipon@gmail.com",
    },
)

app.include_router(base.router)
