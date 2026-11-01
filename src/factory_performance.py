import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "nassau_factory_mapped.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "factory_performance.csv"

df = pd.read_csv(DATA_PATH)

# Factory-level performance
factory_performance = (
    df.groupby("Factory", as_index=False)
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Lead Time", "mean"),
        Minimum_Lead_Time=("Lead Time", "min"),
        Maximum_Lead_Time=("Lead Time", "max"),
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum"),
        Unique_Customers=("Customer ID", "nunique"),
        Unique_States=("State/Province", "nunique")
    )
)

factory_performance["Average_Lead_Time"] = (
    factory_performance["Average_Lead_Time"].round(2)
)

factory_performance = factory_performance.sort_values(
    "Average_Lead_Time"
)

factory_performance.to_csv(OUTPUT_PATH, index=False)

print("\n========== FACTORY PERFORMANCE ==========")

print(factory_performance.to_string(index=False))

print("\nFastest factory by average order-to-ship time:")
print(factory_performance.iloc[0]["Factory"])

print("\nSlowest factory by average order-to-ship time:")
print(factory_performance.iloc[-1]["Factory"])

print("\nSaved:", OUTPUT_PATH)

print("\n========== ANALYSIS COMPLETED ==========")