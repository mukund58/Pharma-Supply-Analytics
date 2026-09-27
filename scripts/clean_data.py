import pandas as pd
import ast
from pathlib import Path


RAW_FILE = "data/drug_shortages_raw.csv"
CLEAN_FILE = "data/drug_shortages_clean.csv"
CATEGORY_FILE = "data/drug_therapeutic_categories.csv"


# --------------------------------------------------
# 1. Load raw FDA data
# --------------------------------------------------

df = pd.read_csv(RAW_FILE)

print(f"Raw records: {len(df)}")


# --------------------------------------------------
# 2. Normalize column names
# --------------------------------------------------

df.columns = (
    df.columns
    .str.lower()
    .str.replace(".", "_", regex=False)
)


# --------------------------------------------------
# 3. Clean text columns
# --------------------------------------------------

text_columns = [
    "package_ndc",
    "generic_name",
    "company_name",
    "presentation",
    "status",
    "update_type",
    "availability",
    "shortage_reason",
    "dosage_form",
    "related_info",
    "resolved_note",
    "related_info_link",
]

for column in text_columns:
    if column in df.columns:
        df[column] = df[column].astype("string").str.strip()


# --------------------------------------------------
# 4. Standardize availability
# --------------------------------------------------

df["availability"] = (
    df["availability"]
    .replace({
        "unavailable": "Unavailable",
        "Unvailable": "Unavailable",
    })
)


# --------------------------------------------------
# 5. Convert dates
# --------------------------------------------------

date_columns = [
    "initial_posting_date",
    "update_date",
    "change_date",
    "discontinued_date",
]

for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )


# --------------------------------------------------
# 6. Create stable event ID
# --------------------------------------------------

df.insert(
    0,
    "event_id",
    range(1, len(df) + 1)
)


# --------------------------------------------------
# 7. Create clean drug table
# --------------------------------------------------

drug_columns = [
    "package_ndc",
    "generic_name",
    "presentation",
    "dosage_form",
    "openfda_brand_name",
    "openfda_product_type",
    "openfda_route",
    "openfda_substance_name",
]

drug_columns = [
    column for column in drug_columns
    if column in df.columns
]

drugs = (
    df[drug_columns]
    .drop_duplicates(subset=["package_ndc"])
    .copy()
)

drugs.to_csv(
    "data/drugs.csv",
    index=False
)


# --------------------------------------------------
# 8. Create company table
# --------------------------------------------------

companies = (
    df[["company_name"]]
    .drop_duplicates()
    .sort_values("company_name")
    .reset_index(drop=True)
)

companies.insert(
    0,
    "company_id",
    range(1, len(companies) + 1)
)

companies.to_csv(
    "data/companies.csv",
    index=False
)


# --------------------------------------------------
# 9. Create therapeutic category table
# --------------------------------------------------

category_rows = []

for _, row in df[["package_ndc", "therapeutic_category"]].iterrows():

    value = row["therapeutic_category"]

    if pd.isna(value):
        continue

    try:
        categories = ast.literal_eval(value)

        if isinstance(categories, list):
            for category in categories:
                category_rows.append({
                    "package_ndc": row["package_ndc"],
                    "therapeutic_category": category
                })

    except (ValueError, SyntaxError):
        pass


categories = pd.DataFrame(category_rows).drop_duplicates()

categories.to_csv(
    CATEGORY_FILE,
    index=False
)


# --------------------------------------------------
# 10. Create supply events table
# --------------------------------------------------

events = df[
    [
        "event_id",
        "package_ndc",
        "company_name",
        "status",
        "update_type",
        "availability",
        "shortage_reason",
        "initial_posting_date",
        "update_date",
        "change_date",
        "discontinued_date",
        "related_info",
        "related_info_link",
        "resolved_note",
        "contact_info",
    ]
].copy()


events.to_csv(
    CLEAN_FILE,
    index=False
)


# --------------------------------------------------
# 11. Summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("=" * 60)

print(f"Drug records:              {len(drugs)}")
print(f"Company records:           {len(companies)}")
print(f"Therapeutic relationships: {len(categories)}")
print(f"Supply events:             {len(events)}")

print("\nFiles created:")

print("  data/drugs.csv")
print("  data/companies.csv")
print("  data/drug_therapeutic_categories.csv")
print("  data/drug_shortages_clean.csv")
