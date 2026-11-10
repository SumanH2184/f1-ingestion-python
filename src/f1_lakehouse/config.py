import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    log_level: str
    request_timeout_seconds: float


def load_settings() -> Settings:
    return Settings(
        data_dir=Path(os.environ.get("F1_DATA_DIR", "data")),
        log_level=os.environ.get("F1_LOG_LEVEL", "INFO").upper(),
        request_timeout_seconds=float(os.environ.get("F1_REQUEST_TIMEOUT", "30")),
    )
