from pathlib import Path
from pydantic_settings import BaseSettings


BASE_PATH = Path(__file__).parent.parent


class Settings(BaseSettings):
    DEBUG: bool
    BOT_TOKEN: str
    DB_DSN: str = "sqlite+aiosqlite:///database.sqllite"


def get_settings() -> Settings:
    return Settings()  # type: ignore
