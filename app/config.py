from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Manages application configuration settings using Pydantic's BaseSettings.

    This class centralizes all the configuration parameters for the application.
    It automatically reads environment variables from a `.env` file and validates
    their types.

    Attributes:
        POSTGRES_USER (str): The username for the PostgreSQL database.
        POSTGRES_PASSWORD (str): The password for the PostgreSQL database.
        POSTGRES_DB (str): The name of the PostgreSQL database.
        REDIS_HOST (str): The hostname for the Redis server. Defaults to 'localhost'.

    Properties:
        DATABASE_URL (str): The fully constructed PostgreSQL connection URL.
        CELERY_BROKER_URL (str): The connection URL for the Celery message broker (Redis).
        CELERY_RESULT_BACKEND (str): The connection URL for the Celery result backend (Redis).

    Config:
        model_config (SettingsConfigDict): Pydantic model configuration.
            - env_file (str): Specifies the file to load environment variables from ('.env').
            - extra (str): Configured to 'ignore', so extra environment variables are ignored.
    """
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    REDIS_HOST: str = 'localhost'

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db/{self.POSTGRES_DB}"

    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:6379/0"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"redis://{self.REDIS_HOST}:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()