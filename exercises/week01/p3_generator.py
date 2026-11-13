# Peak memory, measured with `python exercises/week01/p3_generator.py data/lap_times.csv`:
# List version: 153,990,772 bytes (146.9 MiB); streaming version: 52,496 bytes (51.3 KiB).

from __future__ import annotations

import csv
import sys
import tracemalloc
from collections import Counter
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LapTime:
    race_id: int
    driver_id: int
    lap: int
    milliseconds: int


RawRow = Mapping[str, str | None]

# Supports the usual F1 CSV headers, plus snake_case equivalents.
COLUMN_NAMES: dict[str, tuple[str, ...]] = {
    "race_id": ("raceId", "race_id"),
    "driver_id": ("driverId", "driver_id"),
    "lap": ("lap",),
    "milliseconds": ("milliseconds",),
}


def read_rows(csv_path: Path) -> Iterator[dict[str, str | None]]:
    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        yield from csv.DictReader(csv_file)


def clean(row: RawRow) -> tuple[LapTime | None, str | None]:
    values: dict[str, int] = {}

    for field_name, possible_columns in COLUMN_NAMES.items():
        raw_value = next(
            (row[column] for column in possible_columns if column in row),
            None,
        )

        if raw_value is None or raw_value.strip() == "":
            return None, "missing value"

        try:
            values[field_name] = int(raw_value)
        except ValueError:
            return None, "not a number"

    if values["milliseconds"] <= 0:
        return None, "non-positive time"

    return (
        LapTime(
            race_id=values["race_id"],
            driver_id=values["driver_id"],
            lap=values["lap"],
            milliseconds=values["milliseconds"],
        ),
        None,
    )


def iter_clean_lap_times(
    rows: Iterable[RawRow],
    bad_rows_by_reason: Counter[str],
) -> Iterator[LapTime]:
    """Yield valid rows while recording each rejected row by reason."""

    for row in rows:
        lap_time, reason = clean(row)

        if lap_time is not None:
            yield lap_time
        else:
            bad_rows_by_reason[reason or "unknown error"] += 1


def list_version(csv_path: Path) -> tuple[int, int, Counter[str], int]:
    bad_rows_by_reason: Counter[str] = Counter()
    tracemalloc.start()
    try:
        lap_times = list(iter_clean_lap_times(read_rows(csv_path), bad_rows_by_reason))
        total = sum(lap_time.milliseconds for lap_time in lap_times)
        _, peak_memory = tracemalloc.get_traced_memory()
        return total, len(lap_times), bad_rows_by_reason, peak_memory
    finally:
        tracemalloc.stop()


def streaming_version(csv_path: Path) -> tuple[int, int, Counter[str], int]:
    bad_rows_by_reason: Counter[str] = Counter()
    tracemalloc.start()
    try:
        total = 0
        good_count = 0

        for lap_time in iter_clean_lap_times(read_rows(csv_path), bad_rows_by_reason):
            total += lap_time.milliseconds
            good_count += 1

        _, peak_memory = tracemalloc.get_traced_memory()
        return total, good_count, bad_rows_by_reason, peak_memory
    finally:
        tracemalloc.stop()


def main(csv_path: Path) -> None:
    list_total, list_good_count, list_bad_rows, list_peak = list_version(csv_path)
    streaming_total, streaming_good_count, streaming_bad_rows, streaming_peak = streaming_version(
        csv_path
    )

    list_bad_count = sum(list_bad_rows.values())
    streaming_bad_count = sum(streaming_bad_rows.values())

    assert list_total == streaming_total
    assert list_good_count == streaming_good_count
    assert list_bad_count == streaming_bad_count == 1_000

    print(
        "List version: "
        f"total={list_total}, good rows={list_good_count}, "
        f"bad rows={list_bad_count}, peak memory={list_peak} bytes"
    )
    print(
        "Streaming version: "
        f"total={streaming_total}, good rows={streaming_good_count}, "
        f"bad rows={streaming_bad_count}, peak memory={streaming_peak} bytes"
    )
    print(f"Bad rows by reason: {streaming_bad_rows}")


if __name__ == "__main__":
    sample_rows: list[RawRow] = [
        {"raceId": "1", "driverId": "44", "lap": "2", "milliseconds": "95000"},
        {"raceId": "1", "driverId": "4", "lap": "2", "milliseconds": "fast"},
        {"raceId": "1", "driverId": "16", "lap": "2", "milliseconds": "-95000"},
    ]
    sample_bad_rows: Counter[str] = Counter()
    sample_laps = list(iter_clean_lap_times(sample_rows, sample_bad_rows))

    assert sample_laps == [LapTime(race_id=1, driver_id=44, lap=2, milliseconds=95000)]
    assert sample_bad_rows["not a number"] == 1
    assert sample_bad_rows["non-positive time"] == 1
    assert list(iter_clean_lap_times([], Counter())) == []
    assert clean({"raceId": "1", "driverId": "1", "lap": "1", "milliseconds": "0"}) == (
        None,
        "non-positive time",
    )

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python exercises/week01/p3_generator.py path/to/lap_times.csv")

    main(Path(sys.argv[1]))
