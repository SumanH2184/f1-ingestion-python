import csv
import random
from pathlib import Path

ROWS = 1_000_000
BAD_EVERY = 1000  # one bad row in every 1000

random.seed(42)
path = Path("data/lap_times.csv")
path.parent.mkdir(exist_ok=True)

with path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["race_id", "driver_id", "lap", "milliseconds"])
    for number in range(1, ROWS + 1):
        race_id = random.randint(1, 500)
        driver_id = random.randint(1, 20)
        lap = random.randint(1, 70)
        milliseconds = random.randint(70_000, 120_000)
        if number % BAD_EVERY == 0:
            bad_kind = random.choice(["text", "empty", "negative"])
            if bad_kind == "text":
                writer.writerow([race_id, driver_id, lap, "abc"])
            elif bad_kind == "empty":
                writer.writerow([race_id, "", lap, milliseconds])
            else:
                writer.writerow([race_id, driver_id, lap, -milliseconds])
        else:
            writer.writerow([race_id, driver_id, lap, milliseconds])

print(f"wrote {ROWS} rows to {path}")
