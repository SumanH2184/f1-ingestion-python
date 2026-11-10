import logging

from f1_lakehouse.config import load_settings
from f1_lakehouse.ingestion.pipeline import IngestionResult, ingest_records
from f1_lakehouse.ingestion.readers import read_csv_records
from f1_lakehouse.logging_setup import configure_logging

logger = logging.getLogger(__name__)


def run_ingestion(file_name: str) -> IngestionResult:
    settings = load_settings()
    configure_logging(settings.log_level)

    path = settings.data_dir / file_name
    if not path.is_file():
        raise FileNotFoundError(f"input file not found: {path}")

    logger.info("Starting ingestion from %s", path)
    return ingest_records(read_csv_records(path))
