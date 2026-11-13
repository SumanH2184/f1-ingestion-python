driver = "VER"
wins = 3
print(driver, wins)

lap_times = [95320, 94880, 95010]
print(lap_times[0])
print(len(lap_times))

for time in lap_times:
    print(time)

fastest = lap_times[0]
for time in lap_times:
    if time < fastest:
        fastest = time
print("fastest:", fastest)

lap_points = [10, 8, 6, 5, 4]
largest = lap_points[0]

for point in lap_points:
    if point > largest:
        largest = point
print("largest:", largest)

total = [0]
for points in lap_points:
    total[0] += points
print("total:", total[0])
