import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "nassau_factory_mapped.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "state_analysis.csv"

df = pd.read_csv(DATA_PATH)

# Group by state
state_analysis = (
    df.groupby("State/Province", as_index=False)
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum"),
        Unique_Cities=("City", "nunique"),
        Unique_Factories=("Factory", "nunique")
    )
)

state_analysis["Average_Lead_Time"] = (
    state_analysis["Average_Lead_Time"].round(2)
)

state_analysis = state_analysis.sort_values(
    "Total_Shipments",
    ascending=False
)

state_analysis.to_csv(OUTPUT_PATH, index=False)

print("\n========== GEOGRAPHIC ANALYSIS ==========")

print("\nTop 10 States by Shipment Volume:")

print(
    state_analysis.head(10).to_string(index=False)
)

print("\nTop 10 States by Average Lead Time:")

print(
    state_analysis.sort_values(
        "Average_Lead_Time",
        ascending=False
    ).head(10).to_string(index=False)
)

print("\nTotal States:", len(state_analysis))

print("\nSaved:", OUTPUT_PATH)

print("\n========== ANALYSIS COMPLETED ==========")