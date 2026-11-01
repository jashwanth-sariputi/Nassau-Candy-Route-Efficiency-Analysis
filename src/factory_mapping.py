import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "nassau_cleaned.csv"

df = pd.read_csv(DATA_PATH)

# Product to factory mapping
factory_mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",

    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",

    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",

    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}
# Assign factory
df["Factory"] = df["Product Name"].map(factory_mapping)

# Check mapping
print("\n========== FACTORY MAPPING REPORT ==========")

print("\nProducts without factory mapping:")
print(df[df["Factory"].isna()]["Product Name"].unique())

print("\nFactory Distribution:")
print(df["Factory"].value_counts(dropna=False))

print("\nFactory to Customer Route Sample:")
print(
    df[["Factory", "State/Province", "City", "Product Name"]]
    .head(15)
    .to_string(index=False)
)

print("\n========== MAPPING COMPLETED ==========")

# Save mapped dataset
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "nassau_factory_mapped.csv"

df.to_csv(OUTPUT_PATH, index=False)

print("\nSaved:", OUTPUT_PATH)