
from pathlib import Path
import numpy as np
import pandas as pd

# Reproducible fictional data
rng = np.random.default_rng(42)
N = 10194

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT = BASE_DIR / "data" / "demo" / "nassau_demo.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

factories = [
    "Demo Factory North",
    "Demo Factory South",
    "Demo Factory East",
    "Demo Factory West",
    "Demo Factory Central",
]

factory_names = factories

# Fictional locations
locations = [
    ("United States", "New York", "New York", "East"),
    ("United States", "Los Angeles", "California", "West"),
    ("United States", "Chicago", "Illinois", "Central"),
    ("United States", "Houston", "Texas", "South"),
    ("United States", "Miami", "Florida", "South"),
    ("United States", "Seattle", "Washington", "West"),
    ("United States", "Boston", "Massachusetts", "East"),
    ("United States", "Denver", "Colorado", "West"),
    ("Canada", "Toronto", "Ontario", "East"),
    ("Canada", "Vancouver", "British Columbia", "West"),
]

ship_modes = ["First Class", "Same Day", "Second Class", "Standard Class"]
divisions = ["Chocolate", "Candy", "Gum", "Mints", "Snacks"]

# Factory workload proportions are illustrative, not actual company figures.
# Equal distribution for fictional demo factories
factory_probabilities = np.full(
    len(factory_names), 1 / len(factory_names)
)

selected_factories = rng.choice(
    factory_names, N, p=factory_probabilities
)

selected_locations = rng.integers(0, len(locations), N)

order_dates = (
    pd.Timestamp("2024-01-01")
    + pd.to_timedelta(rng.integers(0, 730, N), unit="D")
)

# Fictional processing intervals, deliberately varied for dashboard analysis.
lead_times = np.clip(
    rng.normal(1320, 170, N).astype(int), 850, 1800
)

ship_dates = order_dates + pd.to_timedelta(lead_times, unit="D")

data = []

for i in range(N):
    country, city, state, region = locations[selected_locations[i]]
    factory = selected_factories[i]

    data.append({
        "Row ID": i + 1,
        "Order ID": f"DEMO-ORD-{i + 1:06d}",
        "Order Date": order_dates[i],
        "Ship Date": ship_dates[i],
        "Ship Mode": rng.choice(ship_modes),
        "Customer ID": f"DEMO-CUST-{rng.integers(1, 1501):05d}",
        "Country/Region": country,
        "City": city,
        "State/Province": state,
        "Postal Code": str(rng.integers(10000, 99999)),
        "Division": rng.choice(divisions),
        "Region": region,
        "Product ID": f"DEMO-PROD-{rng.integers(1, 301):04d}",
        "Product Name": f"Demo Candy Product {rng.integers(1, 301):03d}",
        "Sales": round(float(rng.uniform(20, 1500)), 2),
        "Units": int(rng.integers(1, 30)),
        "Gross Profit": round(float(rng.uniform(2, 450)), 2),
        "Cost": round(float(rng.uniform(5, 800)), 2),
        "Lead Time": int(lead_times[i]),
        "Factory": factory,
    })

df = pd.DataFrame(data)

df.to_csv(OUTPUT, index=False)

print("Synthetic demo dataset created successfully!")
print("File:", OUTPUT)
print("Shape:", df.shape)
print("Columns:", len(df.columns))
print("\nFactory distribution:")
print(df["Factory"].value_counts())
