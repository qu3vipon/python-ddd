from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    detail: str = Field(...)
    result: Any
