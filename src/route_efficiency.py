import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "route_summary.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "route_efficiency.csv"

df = pd.read_csv(DATA_PATH)

# Find minimum and maximum route lead times
min_lead_time = df["Average_Lead_Time"].min()
max_lead_time = df["Average_Lead_Time"].max()

# Calculate relative efficiency score
if max_lead_time == min_lead_time:
    df["Efficiency_Score"] = 100
else:
    df["Efficiency_Score"] = (
        (max_lead_time - df["Average_Lead_Time"])
        / (max_lead_time - min_lead_time)
    ) * 100

df["Efficiency_Score"] = df["Efficiency_Score"].round(2)

# Classify routes
def classify_route(score):
    if score >= 75:
        return "High Efficiency"
    elif score >= 40:
        return "Moderate Efficiency"
    else:
        return "Low Efficiency"

df["Efficiency_Category"] = df["Efficiency_Score"].apply(
    classify_route
)

# Sort routes by efficiency
df = df.sort_values(
    by="Efficiency_Score",
    ascending=False
)

df.to_csv(OUTPUT_PATH, index=False)

print("\n========== ROUTE EFFICIENCY ANALYSIS ==========")

print("\nTop 10 Efficient Routes:")
print(df.head(10)[[
    "Factory",
    "State/Province",
    "City",
    "Average_Lead_Time",
    "Efficiency_Score",
    "Efficiency_Category"
]].to_string(index=False))

print("\nBottom 10 Efficient Routes:")
print(df.tail(10)[[
    "Factory",
    "State/Province",
    "City",
    "Average_Lead_Time",
    "Efficiency_Score",
    "Efficiency_Category"
]].to_string(index=False))

print("\nEfficiency Category Distribution:")
print(df["Efficiency_Category"].value_counts())

print("\nSaved:", OUTPUT_PATH)

print("\n========== ANALYSIS COMPLETED ==========")