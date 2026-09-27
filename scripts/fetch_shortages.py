import requests
import pandas as pd
import time

BASE_URL = "https://api.fda.gov/drug/shortages.json"

LIMIT = 1000

all_records = []
skip = 0

while True:
    params = {
        "limit": LIMIT,
        "skip": skip
    }

    print(f"Fetching records {skip} → {skip + LIMIT}...")

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    records = data.get("results", [])

    if not records:
        break

    all_records.extend(records)

    total = data["meta"]["results"]["total"]

    print(f"Received {len(records)} records")
    print(f"Total available: {total}")

    skip += LIMIT

    if skip >= total:
        break

    time.sleep(0.5)


print(f"\nTotal records downloaded: {len(all_records)}")

df = pd.json_normalize(all_records)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

df.to_csv(
    "data/drug_shortages_raw.csv",
    index=False
)

print("\nSaved to data/drug_shortages_raw.csv")
