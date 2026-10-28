import os
from pathlib import Path
from pydantic import PrivateAttr
from pydantic_settings import BaseSettings, SettingsConfigDict



BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )
    REQUEST_MAX_DELAY: int
    REQUEST_MIN_DELAY: int
    IS_ON_3_SECOND_DELAY: bool

    SUPLIER_ID: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"

    _redis_url: str | None = PrivateAttr(default=None)
    _postgres_url: str | None = PrivateAttr(default=None)
    
    @property
    def REDIS_URL(self):
        if self._redis_url is None:
            self._redis_url = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return self._redis_url

    @property
    def POSTGRES_URL(self) -> str:
        if self._postgres_url is None:
            self._postgres_url = (
                f"postgresql+psycopg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
                f"/{self.POSTGRES_DB}"
            )

        return self._postgres_url

settings = Settings() # type: ignore