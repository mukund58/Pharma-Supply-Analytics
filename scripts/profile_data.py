import pandas as pd

df = pd.read_csv("data/drug_shortages_raw.csv")

print("=" * 70)
print("STATUS × AVAILABILITY")
print("=" * 70)

print(
    pd.crosstab(
        df["status"],
        df["availability"],
        dropna=False
    )
)


print("\n" + "=" * 70)
print("STATUS × SHORTAGE REASON")
print("=" * 70)

print(
    pd.crosstab(
        df["status"],
        df["shortage_reason"].fillna("Missing"),
    )
)


print("\n" + "=" * 70)
print("STATUS × UPDATE TYPE")
print("=" * 70)

print(
    pd.crosstab(
        df["status"],
        df["update_type"]
    )
)


print("\n" + "=" * 70)
print("DUPLICATE PACKAGE NDC")
print("=" * 70)

print(
    "Total records:",
    len(df)
)

print(
    "Unique package NDC:",
    df["package_ndc"].nunique()
)

print(
    "Duplicate package NDC:",
    df["package_ndc"].duplicated().sum()
)


print("\n" + "=" * 70)
print("DATE RANGE")
print("=" * 70)

df["initial_posting_date"] = pd.to_datetime(
    df["initial_posting_date"],
    errors="coerce"
)

df["update_date"] = pd.to_datetime(
    df["update_date"],
    errors="coerce"
)

print(
    "Initial posting:",
    df["initial_posting_date"].min(),
    "→",
    df["initial_posting_date"].max()
)

print(
    "Last update:",
    df["update_date"].min(),
    "→",
    df["update_date"].max()
)


print("\n" + "=" * 70)
print("TOP GENERIC DRUGS")
print("=" * 70)

print(
    df["generic_name"]
    .value_counts()
    .head(20)
)


print("\n" + "=" * 70)
print("TOP DOSAGE FORMS")
print("=" * 70)

print(
    df["dosage_form"]
    .value_counts()
)


print("\n" + "=" * 70)
print("TOP COMPANIES — CURRENT RECORDS")
print("=" * 70)

print(
    df[df["status"] == "Current"]["company_name"]
    .value_counts()
    .head(20)
)
