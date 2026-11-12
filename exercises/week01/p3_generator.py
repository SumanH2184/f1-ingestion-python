from __future__ import annotations

import csv
import sys
import tracemalloc
from collections import Counter
from collections.abc import Callable, Iterable, Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar


@dataclass(frozen=True)
class LapTime:
    race_id: int
    driver_id: int
    lap: int
    milliseconds: int


RawRow = Mapping[str, str | None]
T = TypeVar("T")

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


def collect_clean(
    rows: Iterable[RawRow],
) -> tuple[list[LapTime], Counter[str]]:
    good_rows: list[LapTime] = []
    bad_rows_by_reason: Counter[str] = Counter()

    for row in rows:
        lap_time, reason = clean(row)

        if lap_time is not None:
            good_rows.append(lap_time)
        else:
            bad_rows_by_reason[reason or "unknown error"] += 1

    return good_rows, bad_rows_by_reason


def sum_with_list(lap_times: Iterable[LapTime]) -> int:
    milliseconds = [lap_time.milliseconds for lap_time in lap_times]
    return sum(milliseconds)


def sum_with_generator(lap_times: Iterable[LapTime]) -> int:
    return sum(lap_time.milliseconds for lap_time in lap_times)


def measure(action: Callable[[], T]) -> tuple[T, int]:
    tracemalloc.start()
    try:
        result = action()
        _, peak_memory = tracemalloc.get_traced_memory()
        return result, peak_memory
    finally:
        tracemalloc.stop()


def main(csv_path: Path) -> None:
    lap_times, bad_rows_by_reason = collect_clean(read_rows(csv_path))
    bad_count = sum(bad_rows_by_reason.values())

    list_total, list_peak = measure(lambda: sum_with_list(lap_times))
    generator_total, generator_peak = measure(lambda: sum_with_generator(lap_times))

    assert list_total == generator_total
    assert bad_count == 1_000, f"Expected 1000 bad rows, got {bad_count}"

    print(f"Good rows: {len(lap_times)}")
    print(f"Bad rows: {bad_count}")
    print(f"Bad rows by reason: {bad_rows_by_reason}")
    print(f"List total: {list_total}, peak memory: {list_peak} bytes")
    print(f"Generator total: {generator_total}, peak memory: {generator_peak} bytes")


sample_rows: list[RawRow] = [
    {"raceId": "1", "driverId": "44", "lap": "2", "milliseconds": "95000"},
    {"raceId": "1", "driverId": "4", "lap": "2", "milliseconds": "fast"},
    {"raceId": "1", "driverId": "16", "lap": "2", "milliseconds": "-95000"},
]

sample_laps, sample_bad_rows = collect_clean(sample_rows)

assert sample_laps == [LapTime(race_id=1, driver_id=44, lap=2, milliseconds=95000)]
assert sample_bad_rows["not a number"] == 1
assert sample_bad_rows["non-positive time"] == 1
assert collect_clean([]) == ([], Counter())
assert clean({"raceId": "1", "driverId": "1", "lap": "1", "milliseconds": "0"}) == (
    None,
    "non-positive time",
)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
