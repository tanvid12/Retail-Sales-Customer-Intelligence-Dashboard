
import pandas as pd
import mysql.connector

# Load the cleaned CSV
df = pd.read_csv("data/superstore_clean.csv")
print("CSV shape:", df.shape)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Enter your MySQL root password: "),
    database="retail_sales",
    port=3306
)

cursor = conn.cursor()

# Read the existing table columns
cursor.execute("DESCRIBE orders")
table_columns = [row[0] for row in cursor.fetchall()]

# Ensure the CSV and table columns match
if list(df.columns) != table_columns:
    print("CSV columns:", list(df.columns))
    print("Table columns:", table_columns)
    raise ValueError("Column mismatch. Fix the table before importing.")

# Insert rows in batches
columns_sql = ", ".join(f"`{c}`" for c in df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))
sql = f"INSERT INTO orders ({columns_sql}) VALUES ({placeholders})"

data = [
    tuple(None if pd.isna(v) else v for v in row)
    for row in df.itertuples(index=False, name=None)
]

try:
    for start in range(0, len(data), 500):
        cursor.executemany(sql, data[start:start + 500])
    conn.commit()
    print("Import successful!")
    print("Rows imported:", len(data))
except Exception:
    conn.rollback()
    raise
finally:
    cursor.close()
    conn.close()
