import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nassau Candy | Logistics Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
ORIGINAL_DATA_PATH = (
    BASE_DIR / "data" / "processed" / "nassau_factory_mapped.csv"
)

DEMO_DATA_PATH = (
    BASE_DIR / "data" / "demo" / "nassau_demo.csv"
)

# Use original data locally; use synthetic data when deployed.
DATA_PATH = (
    ORIGINAL_DATA_PATH
    if ORIGINAL_DATA_PATH.exists()
    else DEMO_DATA_PATH
)

# =========================================================
# 2. CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Main application */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        color: #172B4D !important;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #F4F7FB !important;
        color: #172B4D !important;
    }

    /* Main content text */
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] label,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stText"],
    [data-testid="stCaptionContainer"] {
        color: #334155 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #14213D !important;
        font-weight: 700 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #101C36 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Sidebar input fields */
    [data-testid="stSidebar"] [data-baseweb="select"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #172B4D !important;
    }

    /* Header */
    [data-testid="stHeader"] {
        background-color: #F4F7FB !important;
    }

    /* Titles */
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #14213D !important;
        margin-bottom: 2px;
    }

    .subtitle {
        color: #64748B !important;
        font-size: 14px;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: #172B4D !important;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    /* KPI cards */
    .kpi-card {
        background: #FFFFFF !important;
        padding: 19px;
        border-radius: 12px;
        border: 1px solid #E5EAF2;
        box-shadow: 0 3px 12px rgba(20, 33, 61, 0.04);
        min-height: 112px;
    }

    .kpi-label {
        color: #64748B !important;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .kpi-value {
        color: #14213D !important;
        font-size: 25px;
        font-weight: 800;
        margin-top: 9px;
    }

    /* Insights */
    .insight-card {
        background: #FFFFFF !important;
        padding: 16px;
        border-radius: 10px;
        border-left: 4px solid #2878D0;
        margin-bottom: 10px;
        color: #334155 !important;
        border-top: 1px solid #E5EAF2;
        border-right: 1px solid #E5EAF2;
        border-bottom: 1px solid #E5EAF2;
    }

    .insight-card b {
        color: #14213D !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E5EAF2;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #172B4D !important;
    }

    /* Tabs */
    [data-testid="stTabs"] button {
        color: #475569 !important;
        font-weight: 600;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #1769AA !important;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
    }

    /* Download buttons */
    .stDownloadButton button {
        background-color: #1769AA !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
    }

    .stDownloadButton button p {
        color: #FFFFFF !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748B !important;
        padding: 25px 0 10px 0;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. DATA LOADING
# =========================================================

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    required_columns = [
        "Factory", "Order ID", "Order Date", "Ship Date",
        "Ship Mode", "State/Province", "City", "Region",
        "Lead Time", "Sales", "Units"
    ]

    missing = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    data["Order Date"] = pd.to_datetime(
        data["Order Date"], errors="coerce"
    )

    data["Ship Date"] = pd.to_datetime(
        data["Ship Date"], errors="coerce"
    )

    for col in ["Lead Time", "Sales", "Units"]:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

    return data


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()


# =========================================================
# 4. SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("## 🚚 Nassau Candy")
st.sidebar.caption("LOGISTICS INTELLIGENCE PLATFORM")
st.sidebar.divider()

factories = sorted(df["Factory"].dropna().unique())
regions = sorted(df["Region"].dropna().unique())
ship_modes = sorted(df["Ship Mode"].dropna().unique())
states = sorted(df["State/Province"].dropna().unique())
divisions = sorted(df["Division"].dropna().unique())
products = sorted(df["Product Name"].dropna().unique())

with st.sidebar.expander("🏭 Factory", expanded=True):
    selected_factories = st.multiselect(
        "Factory",
        factories,
        default=factories,
        key="factory_filter"
    )

with st.sidebar.expander("🌍 Geography", expanded=False):
    selected_regions = st.multiselect(
        "Region",
        regions,
        default=regions,
        key="region_filter"
    )

    selected_states = st.multiselect(
        "State / Province",
        states,
        key="state_filter"
    )

with st.sidebar.expander("🚚 Shipping", expanded=False):
    selected_modes = st.multiselect(
        "Shipping Mode",
        ship_modes,
        default=ship_modes,
        key="mode_filter"
    )

with st.sidebar.expander("🍬 Products", expanded=False):
    selected_divisions = st.multiselect(
        "Product Division",
        divisions,
        default=divisions,
        key="division_filter"
    )

    selected_products = st.multiselect(
        "Product",
        products,
        default=products,
        key="product_filter"
    )

with st.sidebar.expander("⚙️ Performance Settings", expanded=False):
    threshold = st.slider(
        "Delay Threshold (days)",
        min_value=1,
        max_value=2000,
        value=1300,
        step=10
    )

    minimum_route_volume = st.slider(
        "Minimum Shipments per Route",
        min_value=1,
        max_value=50,
        value=5
    )

    valid_order_dates = df["Order Date"].dropna()

    if not valid_order_dates.empty:
        date_min = valid_order_dates.min().date()
        date_max = valid_order_dates.max().date()

        date_range = st.date_input(
            "Order Date Range",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max
        )
    else:
        date_range = None

if st.sidebar.button("↺ Reset Filters", use_container_width=True):
    for filter_key in [
        "factory_filter",
        "region_filter",
        "state_filter",
        "mode_filter",
        "division_filter",
        "product_filter"
    ]:
        st.session_state.pop(filter_key, None)

    st.rerun()


# =========================================================
# 5. APPLY FILTERS
# =========================================================

filtered_df = df.copy()

# Clean text fields to avoid whitespace mismatches
text_columns = [
    "Factory",
    "Region",
    "Ship Mode",
    "Division",
    "Product Name",
    "State/Province"
]

for col in text_columns:
    filtered_df[col] = filtered_df[col].astype("string").str.strip()
# Normalize selected filter values
selected_factories = [str(x).strip() for x in selected_factories]
selected_regions = [str(x).strip() for x in selected_regions]
selected_modes = [str(x).strip() for x in selected_modes]
selected_divisions = [str(x).strip() for x in selected_divisions]
selected_products = [str(x).strip() for x in selected_products]
selected_states = [str(x).strip() for x in selected_states]

# Apply factory filter
if selected_factories:
    filtered_df = filtered_df[
        filtered_df["Factory"].isin(selected_factories)
    ]

# Apply region filter
if selected_regions:
    filtered_df = filtered_df[
        filtered_df["Region"].isin(selected_regions)
    ]

# Apply shipping mode filter
if selected_modes:
    filtered_df = filtered_df[
        filtered_df["Ship Mode"].isin(selected_modes)
    ]

# Apply product division filter
if selected_divisions:
    filtered_df = filtered_df[
        filtered_df["Division"].isin(selected_divisions)
    ]

# Apply product filter
if selected_products:
    filtered_df = filtered_df[
        filtered_df["Product Name"].isin(selected_products)
    ]

# Apply state/province filter
if selected_states:
    filtered_df = filtered_df[
        filtered_df["State/Province"].isin(selected_states)
    ]

# Apply order date filter
if (
    isinstance(date_range, (tuple, list))
    and len(date_range) == 2
    and date_range[0]
    and date_range[1]
):
    start_date, end_date = date_range

    filtered_df = filtered_df[
        filtered_df["Order Date"].dt.date.between(
            start_date,
            end_date
        )
    ]

# Show filtered record count for debugging
st.sidebar.divider()
st.sidebar.markdown("### Filter Status")
st.sidebar.metric(
    "Remaining Shipment Records",
    f"{len(filtered_df):,}"
)

# Handle empty results
if filtered_df.empty:
    st.warning(
        "No records match your selected filters. "
        "Please change your filter selections."
    )
    st.stop()
# =========================================================
# 6. CALCULATE KPIs
# =========================================================

total_shipments = len(filtered_df)

average_lead = filtered_df["Lead Time"].mean()

total_sales = filtered_df["Sales"].sum()

total_units = filtered_df["Units"].sum()

delayed_count = (
    filtered_df["Lead Time"] > threshold
).sum()

delay_percentage = (
    delayed_count / total_shipments
) * 100

unique_factories = filtered_df["Factory"].nunique()

unique_routes = filtered_df[
    ["Factory", "State/Province", "City"]
].drop_duplicates().shape[0]


# =========================================================
# 7. HEADER
# =========================================================

header_left, header_right = st.columns([4, 1])

with header_left:
    st.markdown(
        '<div class="main-title">Nassau Candy</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Factory-to-Customer Shipping & Route Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        "<div style='text-align:right;color:#64748B;"
        "font-size:12px;padding-top:15px;'>"
        "BUSINESS ANALYTICS"
        "</div>",
        unsafe_allow_html=True
    )

st.divider()


# =========================================================
# 8. EXECUTIVE KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-title">Executive Performance Overview</div>',
    unsafe_allow_html=True
)

kpis = [
    ("TOTAL SHIPMENTS", f"{total_shipments:,}"),
    ("AVERAGE LEAD TIME", f"{average_lead:,.1f} days"),
    ("TOTAL SALES", f"${total_sales:,.2f}"),
    ("TOTAL UNITS", f"{total_units:,.0f}"),
    ("DELAY RATE", f"{delay_percentage:.2f}%")
]

cols = st.columns(5)

for col, (label, value) in zip(cols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.caption(
    "Lead time = Ship Date − Order Date. "
    "It represents order-to-ship processing time, "
    "not confirmed physical transportation or delivery duration."
)

st.write("")


# =========================================================
# 9. AUTOMATED BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">Automated Business Insights</div>',
    unsafe_allow_html=True
)

factory_summary = (
    filtered_df.groupby("Factory")
    .agg(
        Shipments=("Order ID", "count"),
        Average_Lead=("Lead Time", "mean"),
        Sales=("Sales", "sum")
    )
    .reset_index()
)

state_summary = (
    filtered_df.groupby("State/Province")
    .agg(
        Shipments=("Order ID", "count"),
        Average_Lead=("Lead Time", "mean")
    )
    .reset_index()
)

mode_summary = (
    filtered_df.groupby("Ship Mode")
    .agg(
        Shipments=("Order ID", "count"),
        Average_Lead=("Lead Time", "mean")
    )
    .reset_index()
)

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    if (
        not factory_summary.empty
        and factory_summary["Average_Lead"].notna().any()
    ):
        best_factory = factory_summary.loc[
            factory_summary["Average_Lead"].idxmin()
        ]

        st.markdown(
            f"<div class='insight-card'>"
            f"<b>🏭 Lowest Average Lead Time</b><br>"
            f"{best_factory['Factory']} has the lowest observed "
            f"average: {best_factory['Average_Lead']:.2f} days."
            f"</div>",
            unsafe_allow_html=True
        )

    if not factory_summary.empty:
        highest_volume_factory = factory_summary.loc[
            factory_summary["Shipments"].idxmax()
        ]

        st.markdown(
            f"<div class='insight-card'>"
            f"<b>📦 Highest Shipment Volume</b><br>"
            f"{highest_volume_factory['Factory']} handles "
            f"{highest_volume_factory['Shipments']:,} "
            f"shipment records."
            f"</div>",
            unsafe_allow_html=True
        )

with insight_col2:
    if (
        not state_summary.empty
        and state_summary["Average_Lead"].notna().any()
    ):
        slowest_state = state_summary.loc[
            state_summary["Average_Lead"].idxmax()
        ]

        st.markdown(
            f"<div class='insight-card'>"
            f"<b>🌍 Highest Average Lead Time by Geography</b><br>"
            f"{slowest_state['State/Province']} records "
            f"{slowest_state['Average_Lead']:.2f} days across "
            f"{slowest_state['Shipments']} shipment records."
            f"</div>",
            unsafe_allow_html=True
        )

    if (
        not mode_summary.empty
        and mode_summary["Average_Lead"].notna().any()
    ):
        fastest_mode = mode_summary.loc[
            mode_summary["Average_Lead"].idxmin()
        ]

        st.markdown(
            f"<div class='insight-card'>"
            f"<b>🚚 Lowest Average Lead Time by Ship Mode</b><br>"
            f"{fastest_mode['Ship Mode']} records "
            f"{fastest_mode['Average_Lead']:.2f} days on average."
            f"</div>",
            unsafe_allow_html=True
        )

st.divider()


# =========================================================
# 10. ANALYTICS TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🏭 Factory Analytics",
    "🌍 Geographic Analytics",
    "🚚 Shipping Analytics",
    "🛣️ Route Intelligence",
    "🔍 Data Quality"
])


# =========================================================
# TAB 1: OVERVIEW
# =========================================================

with tab1:

    st.markdown("### Monthly Shipment Trends")

    monthly = (
        filtered_df.dropna(subset=["Order Date"])
        .assign(
            Month=lambda x: x["Order Date"].dt.to_period("M").astype(str)
        )
        .groupby("Month")
        .agg(
            Shipments=("Order ID", "count"),
            Sales=("Sales", "sum")
        )
        .reset_index()
    )

    if not monthly.empty:
        chart_left, chart_right = st.columns(2)

        with chart_left:
            fig = px.line(
                monthly,
                x="Month",
                y="Shipments",
                markers=True,
                title="Monthly Shipment Volume",
                template="plotly_white"
            )

            fig.update_traces(
                line=dict(color="#2878D0", width=3),
                marker=dict(size=7)
            )

            fig.update_layout(
                height=380,
                xaxis_title="Order Month",
                yaxis_title="Number of Shipments"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with chart_right:
            fig_sales = px.area(
                monthly,
                x="Month",
                y="Sales",
                title="Monthly Sales Trend",
                template="plotly_white"
            )

            fig_sales.update_traces(
                line_color="#13A89E"
            )

            fig_sales.update_layout(
                height=380,
                xaxis_title="Order Month",
                yaxis_title="Total Sales"
            )

            st.plotly_chart(
                fig_sales,
                use_container_width=True
            )

    st.markdown("### Lead Time Distribution")

    hist_left, hist_right = st.columns(2)

    with hist_left:
        fig_hist = px.histogram(
            filtered_df,
            x="Lead Time",
            nbins=35,
            title="Distribution of Order-to-Ship Lead Time",
            template="plotly_white",
            color_discrete_sequence=["#2878D0"]
        )

        fig_hist.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="red",
            annotation_text="Selected delay threshold"
        )

        fig_hist.update_layout(height=380)

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    with hist_right:
        lead_summary = (
            filtered_df.dropna(subset=["Lead Time"])
            .groupby("Ship Mode")
            .agg(
                Average_Lead_Time=("Lead Time", "mean")
            )
            .reset_index()
            .sort_values("Average_Lead_Time")
        )

        if not lead_summary.empty:
            fig_lead_mode = px.bar(
                lead_summary,
                x="Ship Mode",
                y="Average_Lead_Time",
                color="Average_Lead_Time",
                title="Average Order-to-Ship Time by Ship Mode",
                color_continuous_scale="Teal",
                template="plotly_white"
            )

            fig_lead_mode.update_layout(
                height=380,
                xaxis_title="Shipping Mode",
                yaxis_title="Average Lead Time (days)"
            )

            st.plotly_chart(
                fig_lead_mode,
                use_container_width=True
            )


# =========================================================
# TAB 2: FACTORY ANALYTICS
# =========================================================

with tab2:

    st.markdown("### Factory Performance Comparison")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            factory_summary.sort_values(
                "Shipments",
                ascending=False
            ),
            x="Factory",
            y="Shipments",
            color="Shipments",
            title="Shipment Volume by Factory",
            color_continuous_scale="Blues",
            template="plotly_white"
        )

        fig.update_layout(height=420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:
        fig = px.bar(
            factory_summary.sort_values(
                "Average_Lead",
                ascending=True
            ),
            x="Factory",
            y="Average_Lead",
            color="Average_Lead",
            title="Average Lead Time by Factory",
            color_continuous_scale="Teal",
            template="plotly_white"
        )

        fig.update_layout(height=420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### Factory Performance Table")

    display_factory = factory_summary.copy()

    display_factory["Average_Lead"] = (
        display_factory["Average_Lead"].round(2)
    )

    display_factory["Sales"] = (
        display_factory["Sales"].round(2)
    )

    st.dataframe(
        display_factory,
        use_container_width=True,
        hide_index=True
    )

    # ==========================================
    # PRODUCT-TO-FACTORY WORKLOAD INTELLIGENCE
    # ==========================================

    st.divider()

    st.subheader("Product-to-Factory Workload Intelligence")

    st.caption(
        "Analyse product distribution, factory workload "
        "and product-level business contribution."
    )

    # Aggregate factory and product information
    product_factory_data = (
        filtered_df.groupby(["Factory", "Product Name"])
        .agg(
            Total_Shipments=("Order ID", "count"),
            Total_Units=("Units", "sum"),
            Total_Sales=("Sales", "sum"),
            Average_Lead_Time=("Lead Time", "mean")
        )
        .reset_index()
    )

    # Overall product summary
    product_summary = (
        filtered_df.groupby("Product Name")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Total_Units=("Units", "sum"),
            Total_Sales=("Sales", "sum"),
            Average_Lead_Time=("Lead Time", "mean")
        )
        .reset_index()
        .sort_values("Total_Shipments", ascending=False)
    )

    # KPI calculations
    top_product = product_summary.iloc[0]

    most_units = product_summary.loc[
        product_summary["Total_Units"].idxmax()
    ]

    highest_sales_product = product_summary.loc[
        product_summary["Total_Sales"].idxmax()
    ]

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Products Analysed",
        f"{product_summary['Product Name'].nunique():,}"
    )

    k2.metric(
        "Highest Shipment Product",
        top_product["Product Name"]
    )

    k3.metric(
        "Highest Sales Product",
        highest_sales_product["Product Name"]
    )

    st.divider()

    # Factory-product workload chart
    left, right = st.columns(2)

    with left:
        st.markdown(
            "**Shipment Workload by Factory and Product**"
        )

        workload_pivot = product_factory_data.pivot_table(
            index="Factory",
            columns="Product Name",
            values="Total_Shipments",
            aggfunc="sum",
            fill_value=0
        )

        st.bar_chart(workload_pivot)

    with right:
        st.markdown(
            "**Top 10 Products by Shipment Volume**"
        )

        top_products = product_summary.head(10)

        st.bar_chart(
            top_products.set_index("Product Name")[
                "Total_Shipments"
            ]
        )

    st.divider()

    # Product sales contribution
    st.markdown("**Product Sales Contribution**")

    sales_products = product_summary.sort_values(
        "Total_Sales",
        ascending=False
    ).head(10)

    st.bar_chart(
        sales_products.set_index("Product Name")[
            "Total_Sales"
        ]
    )

    # Factory-product detailed table
    st.markdown("**Factory and Product Performance Details**")

    display_product_data = product_factory_data.copy()

    display_product_data["Average_Lead_Time"] = (
        display_product_data["Average_Lead_Time"].round(2)
    )

    display_product_data["Total_Sales"] = (
        display_product_data["Total_Sales"].round(2)
    )

    display_product_data = display_product_data.sort_values(
        "Total_Shipments",
        ascending=False
    )

    st.dataframe(
        display_product_data,
        use_container_width=True,
        hide_index=True
    )

    # Automatic analytical finding
    st.info(
        f"**Business Insight:** {top_product['Product Name']} "
        f"has the highest shipment volume with "
        f"{int(top_product['Total_Shipments']):,} shipments. "
        f"{highest_sales_product['Product Name']} "
        f"has the highest sales contribution with "
        f"${highest_sales_product['Total_Sales']:,.2f}."
    )


# =========================================================
# TAB 3: GEOGRAPHIC ANALYTICS
# =========================================================

with tab3:

    st.markdown("### Regional Performance")

    c1, c2 = st.columns(2)

    with c1:
        top_states = state_summary.nlargest(
            10,
            "Shipments"
        ).sort_values("Shipments")

        fig = px.bar(
            top_states,
            x="Shipments",
            y="State/Province",
            orientation="h",
            title="Top 10 States / Provinces by Volume",
            template="plotly_white",
            color="Shipments",
            color_continuous_scale="Blues"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:
        slow_states = state_summary.nlargest(
            10,
            "Average_Lead"
        ).sort_values("Average_Lead")

        fig = px.bar(
            slow_states,
            x="Average_Lead",
            y="State/Province",
            orientation="h",
            title="Top 10 by Average Lead Time",
            template="plotly_white",
            color="Average_Lead",
            color_continuous_scale="Reds"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### Geographic Performance Details")

    st.dataframe(
        state_summary.sort_values(
            "Shipments",
            ascending=False
        ).round(2),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Geographic analysis is based on customer State/Province "
        "and City. A physical route map requires verified customer "
        "coordinates, which are not included in the dataset."
    )


# =========================================================
# TAB 4: SHIPPING ANALYTICS
# =========================================================

with tab4:

    st.markdown("### Shipping Mode Performance")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(
            mode_summary,
            names="Ship Mode",
            values="Shipments",
            hole=0.55,
            title="Shipment Share by Shipping Mode",
            template="plotly_white"
        )

        fig.update_layout(height=420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:
        fig = px.bar(
            mode_summary.sort_values("Average_Lead"),
            x="Ship Mode",
            y="Average_Lead",
            color="Average_Lead",
            title="Average Lead Time by Shipping Mode",
            color_continuous_scale="Teal",
            template="plotly_white"
        )

        fig.update_layout(height=420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### Shipping Mode Comparison")

    st.dataframe(
        mode_summary.round(2),
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 5: ROUTE INTELLIGENCE
# =========================================================

with tab5:

    st.markdown("### Factory-to-Customer Route Analysis")

    route_data = (
        filtered_df.groupby(
            ["Factory", "State/Province", "City"]
        )
        .agg(
            Total_Shipments=("Order ID", "count"),
            Average_Lead_Time=("Lead Time", "mean"),
            Total_Sales=("Sales", "sum")
        )
        .reset_index()
    )

    # Relative score based on observed route averages.
    # It is not an externally validated logistics benchmark.

    route_data["Efficiency_Score"] = 0.0

    if len(route_data) > 1:
        lead_min = route_data["Average_Lead_Time"].min()
        lead_max = route_data["Average_Lead_Time"].max()

        if lead_max > lead_min:
            route_data["Efficiency_Score"] = (
                (lead_max - route_data["Average_Lead_Time"])
                / (lead_max - lead_min)
            ) * 100
        else:
            route_data["Efficiency_Score"] = 100.0

    elif len(route_data) == 1:
        route_data["Efficiency_Score"] = 100.0

    route_data["Efficiency_Score"] = (
        route_data["Efficiency_Score"].round(1)
    )

    route_data["Performance"] = pd.cut(
        route_data["Efficiency_Score"],
        bins=[-1, 40, 75, 101],
        labels=["Low", "Moderate", "High"]
    )

    reliable_routes = route_data[
        route_data["Total_Shipments"] >= minimum_route_volume
    ].copy()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Unique Routes",
        f"{len(route_data):,}"
    )

    c2.metric(
        "Routes Meeting Volume Filter",
        f"{len(reliable_routes):,}"
    )

    c3.metric(
        "Average Route Lead Time",
        f"{route_data['Average_Lead_Time'].mean():,.1f} days"
    )

    st.markdown("#### Route Efficiency Ranking")

    if not reliable_routes.empty:

        ranking = reliable_routes.sort_values(
            "Efficiency_Score",
            ascending=False
        ).head(15)

        fig = px.bar(
            ranking.sort_values("Efficiency_Score"),
            x="Efficiency_Score",
            y="City",
            color="Performance",
            orientation="h",
            hover_data=[
                "Factory",
                "State/Province",
                "Total_Shipments",
                "Average_Lead_Time"
            ],
            title="Top 15 Routes by Relative Efficiency Score",
            template="plotly_white",
            color_discrete_map={
                "High": "#16A085",
                "Moderate": "#F4B942",
                "Low": "#E76F51"
            }
        )

        fig.update_layout(height=520)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("#### Route Performance Table")

        st.dataframe(
            reliable_routes.sort_values(
                "Efficiency_Score",
                ascending=False
            ).round(2),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning(
            "No routes meet the selected minimum shipment volume. "
            "Reduce the minimum volume filter."
        )

    st.caption(
        "Efficiency score is a relative comparison of observed "
        "average lead times within the filtered dataset. "
        "It is not a validated industry logistics benchmark."
    )


# =========================================================
# TAB 6: DATA QUALITY AND DELAY ANALYSIS
# =========================================================

with tab6:

    st.markdown("### Data Quality Report")

    missing_values = int(
        filtered_df.isna().sum().sum()
    )

    duplicate_rows = int(
        filtered_df.duplicated().sum()
    )

    invalid_dates = int(
        (
            filtered_df["Order Date"].isna()
            | filtered_df["Ship Date"].isna()
        ).sum()
    )

    nonpositive_lead = int(
        (filtered_df["Lead Time"] <= 0).sum()
    )

    quality1, quality2, quality3, quality4 = st.columns(4)

    quality1.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

    quality2.metric(
        "Duplicate Rows",
        f"{duplicate_rows:,}"
    )

    quality3.metric(
        "Invalid Dates",
        f"{invalid_dates:,}"
    )

    quality4.metric(
        "Non-positive Lead Time",
        f"{nonpositive_lead:,}"
    )

    st.markdown("### Delay Analysis")

    delayed = filtered_df[
        filtered_df["Lead Time"] > threshold
    ]

    on_threshold = filtered_df[
        filtered_df["Lead Time"] <= threshold
    ]

    c1, c2 = st.columns(2)

    with c1:
        delay_data = pd.DataFrame({
            "Status": [
                "Above Threshold",
                "At or Below Threshold"
            ],
            "Shipments": [
                len(delayed),
                len(on_threshold)
            ]
        })

        fig = px.pie(
            delay_data,
            names="Status",
            values="Shipments",
            hole=0.55,
            title=f"Shipments Against {threshold}-Day Threshold",
            template="plotly_white",
            color="Status",
            color_discrete_map={
                "Above Threshold": "#E76F51",
                "At or Below Threshold": "#16A085"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        delay_factory = (
            filtered_df.assign(
                Delayed=filtered_df["Lead Time"] > threshold
            )
            .groupby("Factory")
            .agg(
                Total=("Order ID", "count"),
                Delayed=("Delayed", "sum")
            )
            .reset_index()
        )

        delay_factory["Delay_Percentage"] = (
            delay_factory["Delayed"]
            / delay_factory["Total"]
            * 100
        )

        fig = px.bar(
            delay_factory.sort_values("Delay_Percentage"),
            x="Factory",
            y="Delay_Percentage",
            title="Delay Percentage by Factory",
            color="Delay_Percentage",
            color_continuous_scale="Reds",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### Lead Time Outlier Detection")

    valid_lead = filtered_df.dropna(
        subset=["Lead Time"]
    )

    if not valid_lead.empty:

        q1 = valid_lead["Lead Time"].quantile(0.25)
        q3 = valid_lead["Lead Time"].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = valid_lead[
            (valid_lead["Lead Time"] < lower_bound)
            | (valid_lead["Lead Time"] > upper_bound)
        ]

    else:
        lower_bound = upper_bound = float("nan")
        outliers = valid_lead.copy()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Potential Outliers",
        f"{len(outliers):,}"
    )

    c2.metric(
        "Lower IQR Bound",
        f"{lower_bound:.2f} days"
    )

    c3.metric(
        "Upper IQR Bound",
        f"{upper_bound:.2f} days"
    )

    st.caption(
        "Outliers are flagged using the statistical 1.5 × IQR rule. "
        "They are unusual observations, not automatically confirmed errors."
    )

    if not outliers.empty:

        st.dataframe(
            outliers[
                [
                    "Order ID",
                    "Factory",
                    "State/Province",
                    "City",
                    "Lead Time",
                    "Ship Mode"
                ]
            ].sort_values(
                "Lead Time",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 11. DOWNLOADABLE REPORTS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">Export Business Reports</div>',
    unsafe_allow_html=True
)

download1, download2, download3 = st.columns(3)

with download1:

    st.download_button(
        "⬇ Download Filtered Dataset",
        data=filtered_df.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="nassau_filtered_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

with download2:

    export_routes = (
        filtered_df.groupby(
            ["Factory", "State/Province", "City"]
        )
        .agg(
            Shipments=("Order ID", "count"),
            Average_Lead_Time=("Lead Time", "mean"),
            Total_Sales=("Sales", "sum")
        )
        .reset_index()
    )

    st.download_button(
        "⬇ Download Route Report",
        data=export_routes.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="nassau_route_report.csv",
        mime="text/csv",
        use_container_width=True
    )

with download3:

    st.download_button(
        "⬇ Download Factory Report",
        data=factory_summary.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="nassau_factory_report.csv",
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# 12. FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    <b>NASSAU CANDY | LOGISTICS INTELLIGENCE</b><br>
    Factory-to-Customer Shipping Route Efficiency Analysis<br>
    Data Analytics • Business Intelligence • Operational Insights
</div>
""", unsafe_allow_html=True)