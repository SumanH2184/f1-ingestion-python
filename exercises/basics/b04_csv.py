import csv

with open("cities.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)


print("7" + "32")
print(int("7") + int("32"))

totals = {}
with open("cities.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        country = row["country"]
        population = int(row["population"])
        if country not in totals:
            totals[country] = 0
        totals[country] += population
print(totals)


def points_per_team(path):
    total_points = {}
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            team = row["team"]
            points = int(row["points"])
            if team not in total_points:
                total_points[team] = 0
            total_points[team] += points
    return total_points


print(points_per_team("results.csv"))
