from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).parent.parent.parent / ".env"
_ENV_FILE_ENCODING = "utf-8"

class _EnvConfig(BaseSettings):
    database_url: str
    storage_path: Path = Path(__file__).parent.parent.parent / "storage"

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding=_ENV_FILE_ENCODING,
        extra="ignore"
    )

EnvConfig = _EnvConfig() # type: ignore
