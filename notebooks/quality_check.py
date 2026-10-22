
from pathlib import Path
import pandas as pd

# Locate and load the original dataset
data_folder = Path(__file__).resolve().parent.parent / "data"
files = list(data_folder.glob("*.xls")) + list(data_folder.glob("*.xlsx"))

if not files:
    raise FileNotFoundError("No Excel dataset found in the data folder.")

df = pd.read_excel(files[0])

print("=" * 50)
print("1. DATA TYPES")
print("=" * 50)
print(df.dtypes.to_string())

print("\n" + "=" * 50)
print("2. DUPLICATE RECORDS")
print("=" * 50)
print("Fully duplicated rows:", df.duplicated().sum())
print("Duplicate Row IDs:", df["Row ID"].duplicated().sum())

print("\n" + "=" * 50)
print("3. DATE RANGE")
print("=" * 50)

for column in ["Order Date", "Ship Date"]:
    df[column] = pd.to_datetime(df[column], errors="coerce")
    print(f"{column}: {df[column].min()} to {df[column].max()}")
    print(f"Invalid {column} values:", df[column].isna().sum())

print("\n" + "=" * 50)
print("4. NUMERICAL SUMMARY")
print("=" * 50)
print(df[["Sales", "Quantity", "Discount", "Profit"]].describe().round(2))

print("\n" + "=" * 50)
print("5. BUSINESS CHECKS")
print("=" * 50)
print("Sales <= 0:", (df["Sales"] <= 0).sum())
print("Quantity <= 0:", (df["Quantity"] <= 0).sum())
print("Discount outside 0–1:",
      ((df["Discount"] < 0) | (df["Discount"] > 1)).sum())
print("Loss-making records:", (df["Profit"] < 0).sum())
print("Ship date before order date:",
      (df["Ship Date"] < df["Order Date"]).sum())

print("\nQuality check complete.")


print("\n" + "=" * 50)
print("6. ORDERS BY YEAR")
print("=" * 50)

df["Order Year"] = df["Order Date"].dt.year

print(df.groupby("Order Year").agg(
    Records=("Order ID", "size"),
    Unique_Orders=("Order ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).round(2).to_string())

print("\nEarliest order:")
print(df.loc[df["Order Date"].idxmin(),
             ["Order ID", "Order Date", "Sales", "Profit"]])

print("\nLatest order:")
print(df.loc[df["Order Date"].idxmax(),
             ["Order ID", "Order Date", "Sales", "Profit"]])
