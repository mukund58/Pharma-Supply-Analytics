import pandas as pd

df = pd.read_csv("data/drug_shortages_raw.csv")

print("Shape:", df.shape)

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isna().sum().sort_values(ascending=False))

print("\n" + "=" * 60)
print("STATUS")
print("=" * 60)
print(df["status"].value_counts(dropna=False))

print("\n" + "=" * 60)
print("UPDATE TYPE")
print("=" * 60)
print(df["update_type"].value_counts(dropna=False))

print("\n" + "=" * 60)
print("COMPANIES")
print("=" * 60)
print("Unique companies:", df["company_name"].nunique())
print(df["company_name"].value_counts().head(20))

print("\n" + "=" * 60)
print("THERAPEUTIC CATEGORY")
print("=" * 60)
print(df["therapeutic_category"].value_counts(dropna=False).head(20))

print("\n" + "=" * 60)
print("DOSAGE FORM")
print("=" * 60)
print(df["dosage_form"].value_counts(dropna=False).head(20))

print("\n" + "=" * 60)
print("SHORTAGE REASON")
print("=" * 60)
print(df["shortage_reason"].value_counts(dropna=False))

print("\n" + "=" * 60)
print("AVAILABILITY")
print("=" * 60)
print(df["availability"].value_counts(dropna=False).head(20))
