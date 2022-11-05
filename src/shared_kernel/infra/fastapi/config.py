from typing import ClassVar

from pydantic import BaseSettings


class Settings(BaseSettings):
    DRIVER: ClassVar[str] = "mysql+pymysql"
    USERNAME: ClassVar[str] = "admin"
    PASSWORD: ClassVar[str] = "ddd-hotel"
    HOST: ClassVar[str] = "127.0.0.1"
    PORT: ClassVar[str] = 3306
    DATABASE: ClassVar[str] = "ddd-hotel"

    SQLALCHEMY_DATABASE_URL: ClassVar[str] = f"{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    class Config:
        env_file = ".env"


settings = Settings()
