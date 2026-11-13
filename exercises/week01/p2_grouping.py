from collections import defaultdict


def races_by_season(races: list[tuple[int, str]]) -> dict[int, list[str]]:
    grouped_races: defaultdict[int, list[str]] = defaultdict(list)

    for season, race_name in races:
        grouped_races[season].append(race_name)

    return dict(grouped_races)


def team_to_drivers(driver_teams: dict[str, str]) -> dict[str, list[str]]:
    teams: defaultdict[str, list[str]] = defaultdict(list)

    for driver, team in driver_teams.items():
        teams[team].append(driver)

    for drivers in teams.values():
        drivers.sort()

    return dict(teams)


if __name__ == "__main__":
    assert races_by_season([(2024, "Bahrain"), (2024, "Saudi Arabia"), (2023, "Monaco")]) == {
        2024: ["Bahrain", "Saudi Arabia"],
        2023: ["Monaco"],
    }
    assert races_by_season([(2022, "Monaco")]) == {2022: ["Monaco"]}
    assert races_by_season([]) == {}

    assert team_to_drivers({"VER": "Red Bull", "PER": "Red Bull", "HAM": "Mercedes"}) == {
        "Red Bull": ["PER", "VER"],
        "Mercedes": ["HAM"],
    }
    assert team_to_drivers({"NOR": "McLaren"}) == {"McLaren": ["NOR"]}
    assert team_to_drivers({}) == {}
