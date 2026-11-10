from typing import Any

from f1_lakehouse.models import RaceResult


class ParseError(ValueError):
    """Raised when a raw record cannot be turned into a RaceResult."""


def _require(raw: dict[str, Any], key: str) -> Any:
    if key not in raw or raw[key] in (None, ""):
        raise ParseError(f"missing required field: {key}")
    return raw[key]


def _to_int(raw: dict[str, Any], key: str) -> int:
    value = _require(raw, key)
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ParseError(f"field {key} is not an integer: {value!r}") from exc


def _to_float(raw: dict[str, Any], key: str) -> float:
    value = _require(raw, key)
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ParseError(f"field {key} is not a number: {value!r}") from exc


def parse_race_result(raw: dict[str, Any]) -> RaceResult:
    position = None if raw.get("position") in (None, "") else _to_int(raw, "position")
    return RaceResult(
        season=_to_int(raw, "season"),
        round_number=_to_int(raw, "round_number"),
        race_name=str(_require(raw, "race_name")),
        driver_id=str(_require(raw, "driver_id")),
        constructor_id=str(_require(raw, "constructor_id")),
        grid=_to_int(raw, "grid"),
        position=position,
        points=_to_float(raw, "points"),
        status=str(_require(raw, "status")),
    )
