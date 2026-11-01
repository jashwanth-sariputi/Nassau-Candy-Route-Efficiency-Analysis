# Factory-to-Customer Shipping Route Efficiency Analysis

**Project:** Nassau Candy Distributor – Shipping Route Efficiency Analysis  
**Domain:** Supply Chain Analytics | Logistics | Data Science  
**Tools:** Python, Pandas, NumPy, Plotly, Streamlit

## 1. Project Overview

This project analyzes factory-to-customer shipping route performance for Nassau Candy Distributor. It uses historical shipment records to identify route-level inefficiencies, examine order-to-ship processing times, compare factory performance, and understand geographic shipping patterns.

An interactive Streamlit dashboard presents the findings through KPIs, visualizations, filters, and downloadable reports.

## 2. Business Problem

The business needs better visibility into shipping operations across factories and customer locations.

Without route-level analysis, it can be difficult to:

- Compare performance across factories.
- Identify routes with higher order-to-ship processing times.
- Understand differences between shipping modes.
- Identify geographic areas with relatively slower processing.
- Prioritize routes that may need operational investigation.

## 3. Project Objectives

- Analyze factory-wise shipment performance.
- Evaluate factory-to-customer route efficiency.
- Compare shipping modes using processing-time metrics.
- Identify geographic performance patterns.
- Analyze delayed shipments using a configurable threshold.
- Provide an interactive dashboard for business decision-making.

## 4. Dataset

**Dataset:** Nassau Candy Distributor

The project uses the supplied dataset containing 10,194 shipment records and 18 columns.

The analysis includes shipment, customer, product, sales, cost, date, location, and shipping information.

Factory assignments are derived from the product-to-factory mapping provided in the project brief.

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and application development |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Streamlit | Interactive dashboard |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| OpenPyXL | Spreadsheet support |

## 6. Project Methodology

1. **Data Inspection:** Examine dataset structure, columns, data types, and quality.
2. **Data Cleaning:** Check missing values, duplicate records, date validity, and processing-time values.
3. **Factory Mapping:** Assign factories using the supplied product-to-factory mapping.
4. **Route Analysis:** Aggregate shipment records by factory and customer location.
5. **Factory Performance:** Compare shipment volumes, sales, and average processing times.
6. **Shipping Analysis:** Evaluate performance across shipping modes.
7. **Delay Analysis:** Identify records exceeding the configurable processing-time threshold.
8. **Geographic Analysis:** Examine performance across states, provinces, and regions.
9. **Route Efficiency:** Classify routes using relative processing-time performance.
10. **Dashboard Development:** Present results through an interactive Streamlit application.

## 7. Dashboard Features

The dashboard contains six major sections:

### 1. Overview
- Executive KPI cards.
- Monthly shipment volume.
- Monthly sales trends.
- Lead-time distribution.
- Shipping-mode processing-time comparison.

### 2. Factory Analytics
- Factory-wise shipment performance.
- Sales comparison.
- Average order-to-ship processing time.
- Product-to-factory workload intelligence.

### 3. Geographic Analytics
- Region-wise shipment analysis.
- State and province performance.
- City-level geographic comparisons.
- Geographic bottleneck identification.

### 4. Shipping Analytics
- Shipping-mode comparison.
- Average processing time by shipping mode.
- Shipment volume and sales analysis.

### 5. Route Intelligence
- Factory-to-customer route analysis.
- Route efficiency classification.
- High-, moderate-, and low-efficiency route identification.
- Route-level shipment comparisons.

### 6. Data Quality
- Missing-value checks.
- Duplicate-record checks.
- Date validation.
- Processing-time validation.

## 8. Key Findings

- The dataset contains 10,194 shipment records.
- No missing values or duplicate records were identified during validation.
- Five factories were assigned through the supplied product mapping.
- Lot's O' Nuts and Wicked Choccy's account for the majority of mapped shipment records.
- First Class has the highest average order-to-ship processing time among the four shipping modes.
- 3,379 records (approximately 33.15%) exceed the configurable 1,300-day processing-time threshold.
- The route-efficiency analysis classifies 148 routes as high, 630 as moderate, and 500 as low efficiency.

## 9. Data Limitations and Assumptions

- The dataset does not contain an actual delivery date. Therefore, Lead Time represents the period between Order Date and Ship Date, not actual transportation or delivery duration.
- Factory assignments are derived using the product-to-factory mapping supplied in the project brief.
- The 1,300-day threshold is a configurable analysis threshold, not a confirmed company standard.
- Route-efficiency scores are relative to observed route performance and should not be interpreted as externally validated logistics benchmarks.
- Routes with low shipment volumes may have unstable average processing times.
- The Cost column represents product/manufacturing cost, not freight or transportation cost.

## 10. Project Structure

```text
Nassau_Candy_Project/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── day1_inspection.py
│
└── src/
    ├── data_cleaning.py
    ├── factory_mapping.py
    ├── route_analysis.py
    ├── factory_performance.py
    ├── ship_mode_analysis.py
    ├── delay_analysis.py
    ├── route_efficiency.py
    └── geographic_analysis.py
```

## 11. Installation and Execution

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the project folder

```bash
cd Nassau_Candy_Project
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run the dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open in your default browser.

## 12. Expected Business Value

This project provides a consolidated view of factory-to-customer shipping patterns and processing-time performance.

It helps users:

- Compare factory performance.
- Identify routes that require further investigation.
- Understand geographic processing-time variations.
- Evaluate shipping-mode differences.
- Support data-driven operational discussions.

---

**Project Focus:** Data-driven analysis of factory-to-customer shipping route efficiency using Python and interactive business intelligence visualizations.