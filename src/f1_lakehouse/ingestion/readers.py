import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def read_csv_records(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        yield from reader
