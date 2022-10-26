from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"


settings = Settings()
