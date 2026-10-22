
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

files = (
    list(DATA_DIR.glob("*.xls"))
    + list(DATA_DIR.glob("*.xlsx"))
)

if not files:
    raise FileNotFoundError("No Excel dataset found in data/")

source_file = files[0]
df = pd.read_excel(source_file)

# Standardize column names for easier SQL and Python use
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# Parse dates consistently
for column in ["order_date", "ship_date"]:
    df[column] = pd.to_datetime(df[column], errors="raise")

# Check key data-quality conditions
assert df["row_id"].is_unique, "Duplicate Row IDs found."
assert df["order_date"].notna().all(), "Missing order dates."
assert df["ship_date"].notna().all(), "Missing ship dates."
assert (df["ship_date"] >= df["order_date"]).all(), (
    "Some shipping dates precede order dates."
)

output_file = DATA_DIR / "superstore_clean.csv"
df.to_csv(output_file, index=False, date_format="%Y-%m-%d")

print("Cleaning and export complete.")
print("Source:", source_file.name)
print("Output:", output_file.name)
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
print("Date range:",
      df["order_date"].min().date(),
      "to",
      df["order_date"].max().date())
print("\nStandardized columns:")
print(df.columns.tolist())
