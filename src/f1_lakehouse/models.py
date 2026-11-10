from dataclasses import dataclass


@dataclass(frozen=True)
class RaceResult:
    season: int
    round_number: int
    race_name: str
    driver_id: str
    constructor_id: str
    grid: int
    position: int | None
    points: float
    status: str
