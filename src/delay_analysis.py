import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "nassau_factory_mapped.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "delay_analysis.csv"

df = pd.read_csv(DATA_PATH)

# User-configurable threshold
DELAY_THRESHOLD = 1300

# Identify delayed records
df["Is_Delayed"] = df["Lead Time"] > DELAY_THRESHOLD

# Overall delay analysis
total_shipments = len(df)
delayed_shipments = int(df["Is_Delayed"].sum())

delay_percentage = (
    delayed_shipments / total_shipments
) * 100

print("\n========== OVERALL DELAY ANALYSIS ==========")

print("Delay Threshold:", DELAY_THRESHOLD, "days")
print("Total Records:", total_shipments)
print("Delayed Records:", delayed_shipments)
print("Non-Delayed Records:", total_shipments - delayed_shipments)
print("Delay Percentage:", round(delay_percentage, 2), "%")

# Factory-level delay analysis
factory_delay = (
    df.groupby("Factory", as_index=False)
    .agg(
        Total_Shipments=("Order ID", "count"),
        Delayed_Shipments=("Is_Delayed", "sum")
    )
)

factory_delay["Delay_Percentage"] = (
    factory_delay["Delayed_Shipments"]
    / factory_delay["Total_Shipments"] * 100
).round(2)

factory_delay.to_csv(OUTPUT_PATH, index=False)

print("\n========== FACTORY DELAY ANALYSIS ==========")

print(factory_delay.to_string(index=False))

print("\nSaved:", OUTPUT_PATH)

print("\n========== ANALYSIS COMPLETED ==========")