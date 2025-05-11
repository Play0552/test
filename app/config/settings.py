from typing import Any

from pydantic import Field, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    HOST: str = Field("0.0.0.0", alias="HOST")
    PORT: int = Field(8000, alias="PORT")
    RELOAD: bool = Field(False, alias="RELOAD")
    API_WORKERS: int = Field(1, alias="API_WORKERS")

    # PostgresSQL Configuration
    POSTGRES_DB: str = Field("test", alias="POSTGRES_DB")
    POSTGRES_USER: str = Field("test", alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("test", alias="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field("0.0.0.0", alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, alias="POSTGRES_PORT")

    POSTGRES_DATABASE_URI: PostgresDsn | None = None

    @field_validator("POSTGRES_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            port=values.data.get("POSTGRES_PORT"),
            path=f'{values.data.get("POSTGRES_DB") or ""}',
        )

    # Redis Configuration
    REDIS_HOST: str = Field("0.0.0.0", alias="REDIS_HOST")
    REDIS_PORT: int = Field(6379, alias="REDIS_PORT")
    REDIS_DB: int = Field(0, alias="REDIS_DB")


settings = Settings()
