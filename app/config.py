from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost/{os.getenv("POSTGRES_DB")}"
    CELERY_BROKER_URL: str = f"redis://{os.getenv("REDIS_HOST", "localhost")}:6379/0"
    CELERY_RESULT_BACKEND: str = f"redis://{os.getenv("REDIS_HOST", "localhost")}:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()