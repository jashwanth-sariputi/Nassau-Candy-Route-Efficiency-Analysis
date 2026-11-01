import pandas as pd

# CSV dataset path
DATA_PATH = "data/raw/Nassau Candy Distributor (1).csv"

# Load CSV dataset
df = pd.read_csv(DATA_PATH)

print("\n========== NASSAU CANDY DATASET ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst Five Records:")
print(df.head())

print("\nDataset Information:")
df.info()

print("\n========== DATASET LOADED SUCCESSFULLY ==========")
# ==========================================
# DATA QUALITY INSPECTION
# ==========================================

print("\n========== DATA QUALITY REPORT ==========")

# 1. Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 2. Duplicate records
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# 3. Duplicate Row IDs
print("\nDuplicate Row IDs:")
print(df["Row ID"].duplicated().sum())

# 4. Convert dates into datetime format
df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="%d-%m-%Y", errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], format="%d-%m-%Y", errors="coerce"
)

# 5. Invalid dates
print("\nInvalid Order Dates:")
print(df["Order Date"].isnull().sum())

print("\nInvalid Ship Dates:")
print(df["Ship Date"].isnull().sum())

# 6. Calculate shipment lead time
df["Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print("\nNegative Lead Times:")
print((df["Lead Time"] < 0).sum())

print("\nZero Lead Times:")
print((df["Lead Time"] == 0).sum())

print("\nLead Time Statistics:")
print(df["Lead Time"].describe())

print("\n========== QUALITY INSPECTION COMPLETED ==========")
# ==========================================
# DATE RANGE INVESTIGATION
# ==========================================

print("\n========== DATE RANGE INVESTIGATION ==========")

print("\nOrder Date Range:")
print("Minimum:", df["Order Date"].min())
print("Maximum:", df["Order Date"].max())

print("\nShip Date Range:")
print("Minimum:", df["Ship Date"].min())
print("Maximum:", df["Ship Date"].max())

print("\nOrder Year Distribution:")
print(df["Order Date"].dt.year.value_counts().sort_index())

print("\nShip Year Distribution:")
print(df["Ship Date"].dt.year.value_counts().sort_index())

print("\nSample Records with Lead Time:")
print(
    df[["Order ID", "Order Date", "Ship Date", "Lead Time"]]
    .head(15)
    .to_string(index=False)
)

print("\n========== DATE INVESTIGATION COMPLETED ==========")
# ==========================================
# DATE CONSISTENCY ANALYSIS
# ==========================================

print("\n========== DATE CONSISTENCY ANALYSIS ==========")

# Extract year from Order ID
df["Order ID Year"] = (
    df["Order ID"].str.extract(r"US-(\d{4})")[0]
)

print("\nOrder ID Year Distribution:")
print(df["Order ID Year"].value_counts(dropna=False).sort_index())

print("\nOrder Date Year vs Ship Date Year:")
print(
    pd.crosstab(
        df["Order Date"].dt.year,
        df["Ship Date"].dt.year
    )
)

print("\nLead Time Frequency:")
print(
    df["Lead Time"]
    .value_counts()
    .sort_index()
    .head(20)
)

print("\nUnique Order IDs:")
print(df["Order ID"].nunique())

print("\nUnique Order ID Years:")
print(df["Order ID Year"].nunique())

print("\n========== ANALYSIS COMPLETED ==========")