from dataclasses import dataclass
from typing import ClassVar

from pydantic import BaseSettings


class Settings(BaseSettings):
    DRIVER: ClassVar[str] = "mysql+pymysql"
    USERNAME: ClassVar[str] = "admin"
    PASSWORD: ClassVar[str] = "password"
    HOST: ClassVar[str] = "127.0.0.1"
    PORT: ClassVar[str] = 3306
    DATABASE: ClassVar[str] = "python-ddd"

    SQLALCHEMY_DATABASE_URL: ClassVar[str] = f"{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    class Config:
        env_file = ".env"


settings = Settings()
