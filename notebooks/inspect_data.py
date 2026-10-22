
from pathlib import Path
import pandas as pd

# Locate the data folder
data_folder = Path(__file__).resolve().parent.parent / "data"

# Find Excel files
files = list(data_folder.glob("*.xls")) + list(data_folder.glob("*.xlsx"))

if not files:
    print("No Excel file found in the data folder.")
else:
    file_path = files[0]
    print("Dataset:", file_path.name)

    # Read the first sheet
    df = pd.read_excel(file_path)

    print("\nDataset shape (rows, columns):")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values per column:")
    print(df.isnull().sum())
