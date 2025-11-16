from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError


class Settings(BaseSettings):
    openai_api_key: str = ""
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


try:
    settings = Settings()
except ValidationError as e:
    # Fail fast if required environment variables are missing
    raise RuntimeError(
        f"Configuration error: missing or invalid environment variables.\n{e}"
    )
