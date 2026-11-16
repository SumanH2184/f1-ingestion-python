import csv

print(int("42"))

try:
    number = int("abc")
    print("converted:", number)
except ValueError:
    print("that was not a number")


print("the program keeps running")


def sum_valid(values):
    total = 0
    bad = 0
    for value in values:
        try:
            total += int(value)
        except ValueError:
            bad += 1
    return total, bad


total, bad = sum_valid(["7", "32", "abc", "19", ""])
print("total:", total, "bad:", bad)

prices = {"tea": 10}
try:
    print(prices["coffee"])
except KeyError:
    print("no such key")


def points_per_team_safe(path):
    total_points = {}
    bad_rows = 0
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                team = row["team"]
                points = int(row["points"])
            except ValueError:
                bad_rows += 1
                continue
            if team not in total_points:
                total_points[team] = 0
            total_points[team] += points
    return total_points, bad_rows


total_points, bad_rows = points_per_team_safe("results_bad.csv")
print("total points:", total_points, "bad rows:", bad_rows)
