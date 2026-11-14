def add_tax(price):
    total = price * 1.18
    return total


print(add_tax(100))
print(add_tax(250))


def count_items(items):
    counts = {}
    for item in items:
        if item not in counts:
            counts[item] = 0
        counts[item] += 1
    return counts


fruit_counts = count_items(["apple", "kiwi", "apple"])
print(fruit_counts)
print(count_items(["Pune", "Delhi", "Pune", "Pune"]))


def describe(name, score):
    if score >= 50:
        return f"{name} passed"
    return f"{name} failed"


print(describe("Asha", 72))
print(describe("Ben", 31))


def largest(numbers):
    largest_num = numbers[0]
    for num in numbers:
        if num > largest_num:
            largest_num = num
    return largest_num


print(largest([6, 10, 4, 8, 5]))
print(largest([3, 3, 1]))
print(largest([-5, -2, -9]))


def wins_per_driver(winners):
    winners_counts = {}
    for winner in winners:
        if winner not in winners_counts:
            winners_counts[winner] = 0
        winners_counts[winner] += 1
    return winners_counts


print(wins_per_driver(["VER", "NOR", "VER", "HAM", "NOR", "VER"]))
print(wins_per_driver([]))
