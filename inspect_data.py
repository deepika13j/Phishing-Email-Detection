
import pandas as pd
from pathlib import Path

# Find the project folder
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data" / "raw"

files = ["CEAS_08.csv", "Enron.csv"]

for filename in files:
    file_path = data_folder / filename

    print("\n" + "=" * 50)
    print("Dataset:", filename)

    df = pd.read_csv(file_path, low_memory=False)

    print("Shape (rows, columns):", df.shape)
    print("Columns:", df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3).to_string())

    print("\nMissing values:")
    print(df.isnull().sum())

    if "label" in df.columns:
        print("\nLabel distribution:")
        print(df["label"].value_counts(dropna=False))