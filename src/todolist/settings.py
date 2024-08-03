from pathlib import Path
from pydantic_settings import BaseSettings


BASE_PATH = Path(__file__).parent.parent


class Settings(BaseSettings):
    DEBUG: bool

    BOT_TOKEN: str


def get_settings() -> Settings:
    return Settings()  # type: ignore
