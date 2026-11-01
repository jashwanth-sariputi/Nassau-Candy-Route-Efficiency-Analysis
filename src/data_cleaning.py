import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = BASE_DIR / "data" / "raw" / "Nassau Candy Distributor (1).csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "nassau_cleaned.csv"

# Load original dataset
df = pd.read_csv(RAW_PATH)

# Convert date columns
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Calculate order-to-ship processing time
df["Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Remove records with invalid dates
df = df.dropna(subset=["Order Date", "Ship Date"])

# Remove negative lead times
df = df[df["Lead Time"] >= 0]

# Save processed dataset
df.to_csv(OUTPUT_PATH, index=False)

print("DATA PREPARATION COMPLETED")
print("Remaining records:", len(df))
print("Saved file:", OUTPUT_PATH)
print("\nLead Time Summary:")
print(df["Lead Time"].describe())