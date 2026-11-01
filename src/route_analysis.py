import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "nassau_factory_mapped.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "route_summary.csv"

df = pd.read_csv(DATA_PATH)

# Group records by factory and customer location
route_summary = (
    df.groupby(
        ["Factory", "State/Province", "City"],
        as_index=False
    )
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Lead Time", "mean"),
        Minimum_Lead_Time=("Lead Time", "min"),
        Maximum_Lead_Time=("Lead Time", "max"),
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum")
    )
)

# Round average lead time
route_summary["Average_Lead_Time"] = (
    route_summary["Average_Lead_Time"].round(2)
)

# Sort by shipment volume
route_summary = route_summary.sort_values(
    by="Total_Shipments",
    ascending=False
)

route_summary.to_csv(OUTPUT_PATH, index=False)

print("\n========== ROUTE ANALYSIS ==========")

print("\nTotal Factory-to-Customer Routes:")
print(len(route_summary))

print("\nTop 10 Routes by Shipment Volume:")
print(route_summary.head(10).to_string(index=False))

print("\nBottom 10 Routes by Shipment Volume:")
print(route_summary.tail(10).to_string(index=False))

print("\nSaved:", OUTPUT_PATH)

print("\n========== ANALYSIS COMPLETED ==========")