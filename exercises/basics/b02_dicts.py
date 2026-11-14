capitals = {"India": "Delhi", "Japan": "Tokyo"}
print(capitals["India"])

capitals["France"] = "Paris"
print(capitals)
print(len(capitals))

print("Japan" in capitals)
print("brazil" in capitals)

for country, city in capitals.items():
    print(country, "->", city)

fruits = ["apple", "kiwi", "apple", "fig", "kiwi", "apple"]
counts = {}
for fruit in fruits:
    if fruit not in counts:
        counts[fruit] = 0
    counts[fruit] += 1
print(counts)


winners = ["VER", "NOR", "VER", "HAM", "NOR", "VER"]
winner_counts = {}
for winner in winners:
    if winner not in winner_counts:
        winner_counts[winner] = 0
    winner_counts[winner] += 1
print(winner_counts)
print(winner_counts["VER"])

for driver, count in winner_counts.items():
    print(f"{driver} has {count} wins")
print(count)
