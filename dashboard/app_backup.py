
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="📊",
    layout="wide",
)

# ---------------- LOAD DATA ----------------
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "superstore_clean.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

    for col in ["sales", "profit", "quantity", "discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("📊 Sales Analytics")
st.sidebar.caption("Retail Sales & Customer Intelligence")

regions = sorted(df["region"].dropna().unique())
categories = sorted(df["category"].dropna().unique())
segments = sorted(df["segment"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Region", regions, default=regions
)
selected_categories = st.sidebar.multiselect(
    "Category", categories, default=categories
)
selected_segments = st.sidebar.multiselect(
    "Customer Segment", segments, default=segments
)

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

filtered = df[
    df["region"].isin(selected_regions)
    & df["category"].isin(selected_categories)
    & df["segment"].isin(selected_segments)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["order_date"].dt.date.between(start_date, end_date)
    ]

# ---------------- HEADER ----------------
st.title("Retail Sales & Customer Intelligence Dashboard")
st.markdown(
    "Explore sales performance, profitability, customer segments, "
    "product categories, and shipping efficiency."
)

if filtered.empty:
    st.warning("No records match these filters. Adjust the sidebar selections.")
    st.stop()

# ---------------- KPI CARDS ----------------
total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()
total_orders = filtered["order_id"].nunique()
total_customers = filtered["customer_id"].nunique()
total_quantity = filtered["quantity"].sum()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Unique Customers", f"{total_customers:,}")
c5.metric("Units Sold", f"{total_quantity:,.0f}")

st.divider()

# ---------------- SALES TREND ----------------
st.subheader("Monthly Sales & Profit Trend")

monthly = (
    filtered.assign(
        month=filtered["order_date"].dt.to_period("M").dt.to_timestamp()
    )
    .groupby("month", as_index=False)
    .agg(sales=("sales", "sum"), profit=("profit", "sum"))
    .sort_values("month")
)

fig_trend = px.line(
    monthly,
    x="month",
    y=["sales", "profit"],
    markers=True,
    labels={"month": "Month", "value": "Amount ($)", "variable": "Metric"},
    template="plotly_white",
)
fig_trend.update_layout(legend_title_text="")
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------- CATEGORY AND REGION ----------------
left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    category_data = (
        filtered.groupby("category", as_index=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
        .sort_values("sales", ascending=False)
    )

    fig_category = px.bar(
        category_data,
        x="category",
        y="sales",
        color="category",
        text_auto=".2s",
        labels={"category": "Category", "sales": "Sales ($)"},
        template="plotly_white",
    )
    st.plotly_chart(fig_category, use_container_width=True)

with right:
    st.subheader("Sales by Region")
    region_data = (
        filtered.groupby("region", as_index=False)
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
        .sort_values("sales", ascending=False)
    )

    fig_region = px.bar(
        region_data,
        x="region",
        y="sales",
        color="region",
        text_auto=".2s",
        labels={"region": "Region", "sales": "Sales ($)"},
        template="plotly_white",
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ---------------- PROFITABILITY ----------------
left, right = st.columns(2)

with left:
    st.subheader("Profit by Sub-Category")
    subcategory_data = (
        filtered.groupby("sub_category", as_index=False)
        .agg(profit=("profit", "sum"))
        .sort_values("profit")
    )

    fig_profit = px.bar(
        subcategory_data,
        x="profit",
        y="sub_category",
        orientation="h",
        color="profit",
        color_continuous_scale="RdYlGn",
        labels={"profit": "Profit ($)", "sub_category": "Sub-Category"},
        template="plotly_white",
    )
    st.plotly_chart(fig_profit, use_container_width=True)

with right:
    st.subheader("Sales by Customer Segment")
    segment_data = (
        filtered.groupby("segment", as_index=False)
        .agg(sales=("sales", "sum"))
        .sort_values("sales", ascending=False)
    )

    fig_segment = px.pie(
        segment_data,
        names="segment",
        values="sales",
        hole=0.45,
        template="plotly_white",
    )
    st.plotly_chart(fig_segment, use_container_width=True)

# ---------------- SHIPPING ANALYSIS ----------------
st.subheader("Shipping Performance")

shipping = filtered.dropna(subset=["order_date", "ship_date"]).copy()
shipping["shipping_days"] = (
    shipping["ship_date"] - shipping["order_date"]
).dt.days

shipping_data = (
    shipping.groupby("ship_mode", as_index=False)
    .agg(
        sales=("sales", "sum"),
        avg_shipping_days=("shipping_days", "mean"),
        orders=("order_id", "nunique"),
    )
)

fig_shipping = px.bar(
    shipping_data,
    x="ship_mode",
    y="avg_shipping_days",
    color="ship_mode",
    text_auto=".2f",
    labels={
        "ship_mode": "Shipping Mode",
        "avg_shipping_days": "Average Shipping Days",
    },
    template="plotly_white",
)
st.plotly_chart(fig_shipping, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.subheader("Filtered Order Records")

search = st.text_input("Search by order ID, customer, or product")

display_data = filtered.copy()

if search.strip():
    term = search.strip().lower()
    mask = (
        display_data["order_id"].astype(str).str.lower().str.contains(term, na=False)
        | display_data["customer_name"].astype(str).str.lower().str.contains(term, na=False)
        | display_data["product_name"].astype(str).str.lower().str.contains(term, na=False)
    )
    display_data = display_data[mask]

st.caption(f"{len(display_data):,} records displayed")

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True,
)

csv_data = display_data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Data (CSV)",
    data=csv_data,
    file_name="filtered_retail_sales.csv",
    mime="text/csv",
)

st.caption("Retail Sales & Customer Intelligence | Built with Python, SQL, Streamlit and Plotly")
