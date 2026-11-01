import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "nassau_factory_mapped.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "ship_mode_performance.csv"

df = pd.read_csv(DATA_PATH)

ship_mode_analysis = (
    df.groupby("Ship Mode", as_index=False)
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Lead Time", "mean"),
        Minimum_Lead_Time=("Lead Time", "min"),
        Maximum_Lead_Time=("Lead Time", "max"),
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum"),
        Unique_Customers=("Customer ID", "nunique")
    )
)

ship_mode_analysis["Average_Lead_Time"] = (
    ship_mode_analysis["Average_Lead_Time"].round(2)
)

ship_mode_analysis.to_csv(OUTPUT_PATH, index=False)

print("\n========== SHIP MODE PERFORMANCE ==========")

print(ship_mode_analysis.to_string(index=False))

print("\nSaved:", OUTPUT_PATH)

print("\n========== ANALYSIS COMPLETED ==========")