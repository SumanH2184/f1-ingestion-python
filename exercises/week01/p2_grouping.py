def races_by_season(races: list[tuple[int, str]]) -> dict[int, list[str]]:
    grouped_races: dict[int, list[str]] = {}

    for season, race_name in races:
        if season not in grouped_races:
            grouped_races[season] = []
        grouped_races[season].append(race_name)

    return grouped_races


def team_to_drivers(driver_teams: dict[str, str]) -> dict[str, list[str]]:
    teams: dict[str, list[str]] = {}

    for driver, team in driver_teams.items():
        if team not in teams:
            teams[team] = []
        teams[team].append(driver)

    for drivers in teams.values():
        drivers.sort()

    return teams


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
