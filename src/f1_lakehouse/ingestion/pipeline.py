import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from f1_lakehouse.ingestion.parsing import ParseError, parse_race_result
from f1_lakehouse.models import RaceResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RejectedRecord:
    record_number: int
    reason: str
    raw: dict[str, Any]


@dataclass
class IngestionResult:
    accepted: list[RaceResult] = field(default_factory=list)
    rejected: list[RejectedRecord] = field(default_factory=list)


def ingest_records(raw_records: Iterable[dict[str, Any]]) -> IngestionResult:
    result = IngestionResult()
    for number, raw in enumerate(raw_records, start=1):
        try:
            result.accepted.append(parse_race_result(raw))
        except ParseError as exc:
            logger.warning("Rejected record %d: %s", number, exc)
            result.rejected.append(RejectedRecord(number, str(exc), raw))
    logger.info(
        "Ingestion finished: %d accepted, %d rejected",
        len(result.accepted),
        len(result.rejected),
    )
    return result
