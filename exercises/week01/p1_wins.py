from collections import Counter


def top_three_drivers(winners: list[str]) -> list[tuple[str, int]]:
    win_counts = Counter(winners)
    return sorted(win_counts.items(), key=lambda item: (-item[1], item[0]))[:3]


if __name__ == "__main__":
    assert top_three_drivers(["VER", "VER", "VER", "LEC", "NOR"]) == [
        ("VER", 3),
        ("LEC", 1),
        ("NOR", 1),
    ]
    assert top_three_drivers(["HAM", "RUS", "HAM", "RUS"]) == [
        ("HAM", 2),
        ("RUS", 2),
    ]
    assert top_three_drivers([]) == []
    # YOUR ASSERT HERE: four or more different winners, so one is cut off by [:3]
