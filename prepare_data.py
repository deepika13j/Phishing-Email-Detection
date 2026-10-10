
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Input files
ceas_file = RAW_DIR / "CEAS_08.csv"
enron_file = RAW_DIR / "Enron.csv"

# Output file
output_file = PROCESSED_DIR / "phishing_emails.csv"

def prepare_ceas():
    print("Loading CEAS_08 dataset...")

    df = pd.read_csv(ceas_file)

    # Combine subject and body
    df["subject"] = df["subject"].fillna("").astype(str)
    df["body"] = df["body"].fillna("").astype(str)
    df["text"] = df["subject"] + " " + df["body"]

    # Keep only required columns
    df = df[["text", "label"]]

    return df


def prepare_enron():
    print("Loading Enron dataset...")

    df = pd.read_csv(enron_file)

    # Combine subject and body
    df["subject"] = df["subject"].fillna("").astype(str)
    df["body"] = df["body"].fillna("").astype(str)
    df["text"] = df["subject"] + " " + df["body"]

    # Keep only required columns
    df = df[["text", "label"]]

    return df


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Load both datasets
    ceas = prepare_ceas()
    enron = prepare_enron()

    # Combine datasets
    df = pd.concat([ceas, enron], ignore_index=True)

    # Remove empty emails
    df["text"] = df["text"].fillna("").astype(str).str.strip()
    df = df[df["text"] != ""]

    # Clean labels
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    # Normalize text to identify duplicates
    df["text_key"] = (
        df["text"]
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Remove duplicate emails, including capitalization
    # and whitespace differences
    before = len(df)
    df = df.drop_duplicates(subset="text_key", keep="first")
    removed = before - len(df)

    # Remove temporary column
    df = df.drop(columns=["text_key"])

    # Save processed dataset
    df.to_csv(output_file, index=False)

    # Display results
    print("\nData preparation completed!")
    print("Total emails:", len(df))
    print("Duplicate emails removed:", removed)
    print("\nLabel distribution:")
    print(df["label"].value_counts().sort_index())
    print("\nSaved to:", output_file)


if __name__ == "__main__":
    main()
