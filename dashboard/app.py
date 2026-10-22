
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# DESIGN SYSTEM
# =====================================================
NAVY = "#14213D"
BLUE = "#3B82F6"
TEAL = "#0F9D8A"
ORANGE = "#F59E0B"
RED = "#DC5A5A"
MUTED = "#64748B"
GRID = "#E8EDF4"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: #F6F8FC;
    }}

    [data-testid="stSidebar"] {{
        background-color: #FFFFFF;
        border-right: 1px solid #E5EAF2;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: #475569;
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }}

    .hero {{
        background: linear-gradient(115deg, #14213D 0%, #243F70 100%);
        padding: 30px 34px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(20, 33, 61, 0.10);
    }}

    .hero h1 {{
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: -0.8px;
    }}

    .hero p {{
        color: #D8E3F4;
        font-size: 14px;
        margin: 0;
        line-height: 1.7;
    }}

    .section-heading {{
        color: #14213D;
        font-size: 20px;
        font-weight: 700;
        margin: 12px 0 14px 0;
    }}

    .section-subtitle {{
        color: #64748B;
        font-size: 12px;
        margin-top: -8px;
        margin-bottom: 18px;
    }}

    .kpi-card {{
        background: #FFFFFF;
        padding: 20px 20px 18px 20px;
        border: 1px solid #E6EBF3;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(20, 33, 61, 0.035);
        min-height: 125px;
    }}

    .kpi-label {{
        font-size: 12px;
        color: #64748B;
        font-weight: 600;
        margin-bottom: 12px;
    }}

    .kpi-value {{
        color: #14213D;
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.8px;
        overflow-wrap: anywhere;
    }}

    .kpi-accent {{
        height: 4px;
        width: 38px;
        border-radius: 8px;
        margin-top: 13px;
    }}

    div[data-testid="stPlotlyChart"] {{
        background: #FFFFFF;
        border: 1px solid #E6EBF3;
        border-radius: 15px;
        padding: 8px;
        box-shadow: 0 3px 12px rgba(20, 33, 61, 0.025);
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid #E6EBF3;
        border-radius: 12px;
        overflow: hidden;
    }}

    .retail-table-wrapper {{
        max-height: 520px;
        overflow: auto;
        border: 1px solid #E6EBF3;
        border-radius: 12px;
        background: #FFFFFF;
    }}

    .retail-table-wrapper table {{
        border-collapse: collapse;
        width: 100%;
        font-size: 12px;
        white-space: nowrap;
    }}

    .retail-table-wrapper thead th {{
        position: sticky;
        top: 0;
        z-index: 1;
        background: #EEF3FA;
        color: #14213D;
        text-align: left;
        padding: 10px 12px;
        border-bottom: 1px solid #D9E2EF;
    }}

    .retail-table-wrapper tbody td {{
        padding: 8px 12px;
        border-bottom: 1px solid #EEF2F7;
        color: #334155;
    }}

    .retail-table-wrapper tbody tr:nth-child(even) {{
        background: #F8FAFD;
    }}

    .insight-card {{
        background: white;
        border: 1px solid #E6EBF3;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 10px;
    }}

    .insight-label {{
        color: #64748B;
        font-size: 12px;
        font-weight: 600;
    }}

    .insight-value {{
        color: #14213D;
        font-size: 20px;
        font-weight: 800;
        margin-top: 7px;
    }}

    .footer {{
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        padding: 28px 0 8px 0;
    }}

    div[data-testid="stMetric"] {{
        background: #FFFFFF;
        border: 1px solid #E6EBF3;
        border-radius: 12px;
        padding: 12px 14px;
    }}

    h2, h3 {{
        color: #14213D;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# DATA LOADING
# =====================================================
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "superstore_clean.csv"
)


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    data["order_date"] = pd.to_datetime(
        data["order_date"], errors="coerce"
    )
    data["ship_date"] = pd.to_datetime(
        data["ship_date"], errors="coerce"
    )

    for col in ["sales", "profit", "quantity", "discount"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


try:
    df = load_data()
except Exception as exc:
    st.error(f"Unable to load the dataset: {exc}")
    st.stop()

if df.empty or df["order_date"].dropna().empty:
    st.error("The dataset is empty or has no valid order dates.")
    st.stop()

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 8px 0 20px 0;">
            <div style="font-size: 28px;">📊</div>
            <div style="font-size: 21px; font-weight: 800;
                        color: {NAVY};">Sales Intelligence</div>
            <div style="font-size: 12px; color: {MUTED};
                        margin-top: 5px;">
                RETAIL PERFORMANCE ANALYTICS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("#### Filter your data")

    regions = sorted(df["region"].dropna().unique().tolist())
    categories = sorted(df["category"].dropna().unique().tolist())
    segments = sorted(df["segment"].dropna().unique().tolist())

    selected_regions = st.multiselect(
        "Region",
        regions,
        default=regions,
    )

    selected_categories = st.multiselect(
        "Product Category",
        categories,
        default=categories,
    )

    selected_segments = st.multiselect(
        "Customer Segment",
        segments,
        default=segments,
    )

    valid_dates = df["order_date"].dropna()
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="order_date_range",
    )

    st.divider()

    if st.button("Reset all filters", use_container_width=True):
        st.rerun()

    st.markdown(
        f"""
        <div style="font-size: 11px; color: {MUTED};
                    line-height: 1.8; padding-top: 12px;">
            <b>DATASET</b><br>
            {len(df):,} source records<br>
            {len(df.columns)} data fields
        </div>
        """,
        unsafe_allow_html=True,
    )

# =====================================================
# APPLY FILTERS
# =====================================================
filtered = df[
    df["region"].isin(selected_regions)
    & df["category"].isin(selected_categories)
    & df["segment"].isin(selected_segments)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["order_date"].dt.date.between(
            start_date, end_date
        )
    ]

# =====================================================
# HEADER
# =====================================================
st.markdown(
    """
    <div class="hero">
        <h1>Retail Sales & Customer Intelligence</h1>
        <p>
            A data-driven view of revenue, profitability, customer behavior,
            product performance, and shipping efficiency.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"Reporting period: {start_date if len(date_range) == 2 else min_date} "
    f"to {end_date if len(date_range) == 2 else max_date}"
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2
    else f"Available data: {min_date} to {max_date}"
)

if filtered.empty:
    st.warning(
        "No records match the selected filters. "
        "Adjust your selections in the sidebar."
    )
    st.stop()

# =====================================================
# KPI CARDS
# =====================================================
total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()
total_orders = filtered["order_id"].nunique()
total_customers = filtered["customer_id"].nunique()
total_quantity = filtered["quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100 if total_sales else 0
)

kpis = [
    ("TOTAL SALES", f"${total_sales:,.0f}", BLUE),
    ("TOTAL PROFIT", f"${total_profit:,.0f}", TEAL),
    ("TOTAL ORDERS", f"{total_orders:,}", ORANGE),
    ("UNIQUE CUSTOMERS", f"{total_customers:,}", "#8B5CF6"),
    ("UNITS SOLD", f"{total_quantity:,.0f}", RED),
]

columns = st.columns(5)

for column, (label, value, accent) in zip(columns, kpis):
    with column:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-accent" style="background:{accent};"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

m1, m2 = st.columns(2)

m1.metric("Overall Profit Margin", f"{profit_margin:.2f}%")
m2.metric(
    "Average Order Value",
    f"${total_sales / total_orders:,.2f}" if total_orders else "$0.00",
)

# =====================================================
# SHARED CHART STYLE
# =====================================================
def style_chart(fig, height=360):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=18, r=18, t=35, b=18),
        font=dict(family="Inter, sans-serif", color=NAVY, size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor=GRID)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)
    return fig


# =====================================================
# MONTHLY TREND
# =====================================================
st.markdown(
    '<div class="section-heading">Revenue & Profit Trends</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-subtitle">'
    'Track monthly financial performance across the selected period.'
    '</div>',
    unsafe_allow_html=True,
)

monthly = (
    filtered.assign(
        month=filtered["order_date"].dt.to_period("M").dt.to_timestamp()
    )
    .groupby("month", as_index=False)
    .agg(sales=("sales", "sum"), profit=("profit", "sum"))
    .sort_values("month")
)

fig_trend = go.Figure()

fig_trend.add_trace(
    go.Scatter(
        x=monthly["month"],
        y=monthly["sales"],
        name="Sales",
        mode="lines+markers",
        line=dict(color=BLUE, width=3),
        marker=dict(size=6),
        hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>",
    )
)

fig_trend.add_trace(
    go.Scatter(
        x=monthly["month"],
        y=monthly["profit"],
        name="Profit",
        mode="lines+markers",
        line=dict(color=TEAL, width=3),
        marker=dict(size=6),
        hovertemplate="%{x|%b %Y}<br>Profit: $%{y:,.2f}<extra></extra>",
    )
)

fig_trend.update_layout(
    yaxis_title="Amount ($)",
    xaxis_title="",
    hovermode="x unified",
)
style_chart(fig_trend, 410)
st.plotly_chart(fig_trend, use_container_width=True)

# =====================================================
# CATEGORY AND REGIONAL ANALYSIS
# =====================================================
st.markdown(
    '<div class="section-heading">Sales Performance Breakdown</div>',
    unsafe_allow_html=True,
)

left, right = st.columns(2)

category_data = (
    filtered.groupby("category", as_index=False)
    .agg(sales=("sales", "sum"), profit=("profit", "sum"))
    .sort_values("sales", ascending=True)
)

with left:
    fig_category = px.bar(
        category_data,
        x="sales",
        y="category",
        orientation="h",
        text_auto=",.0f",
        color="category",
        color_discrete_sequence=[BLUE, TEAL, ORANGE],
        labels={
            "sales": "Sales ($)",
            "category": "",
        },
    )

    fig_category.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig_category.update_layout(
        showlegend=False,
        xaxis_title="Sales ($)",
    )

    style_chart(fig_category, 330)

    # Reserve space for the full sales labels
    max_sales = category_data["sales"].max()

    fig_category.update_xaxes(
        range=[0, max_sales * 1.25],
        separatethousands=True,
    )

    fig_category.update_layout(
        margin=dict(l=18, r=65, t=35, b=18),
    )

    st.markdown("**Sales by Product Category**")
    st.plotly_chart(
        fig_category,
        use_container_width=True,
    )
# =====================================================
# PROFIT AND CUSTOMER SEGMENTS
# =====================================================
st.markdown(
    '<div class="section-heading">Profitability & Customer Insights</div>',
    unsafe_allow_html=True,
)

left, right = st.columns(2)

subcategory_data = (
    filtered.groupby("sub_category", as_index=False)
    .agg(sales=("sales", "sum"), profit=("profit", "sum"))
    .sort_values("profit", ascending=True)
)

with left:
    colors = [
        RED if value < 0 else TEAL
        for value in subcategory_data["profit"]
    ]

    fig_profit = go.Figure(
        go.Bar(
            x=subcategory_data["profit"],
            y=subcategory_data["sub_category"],
            orientation="h",
            marker_color=colors,
            hovertemplate="%{y}<br>Profit: $%{x:,.2f}<extra></extra>",
        )
    )
    fig_profit.add_vline(x=0, line_color=NAVY, line_width=1)
    fig_profit.update_layout(
        xaxis_title="Profit ($)",
        yaxis_title="",
    )
    style_chart(fig_profit, 470)

    st.markdown("**Profit by Sub-Category**")
    st.plotly_chart(fig_profit, use_container_width=True)

segment_data = (
    filtered.groupby("segment", as_index=False)
    .agg(sales=("sales", "sum"))
    .sort_values("sales", ascending=False)
)

with right:
    fig_segment = px.pie(
        segment_data,
        names="segment",
        values="sales",
        hole=0.62,
        color_discrete_sequence=[BLUE, TEAL, ORANGE],
    )
    fig_segment.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}<br>Sales: $%{value:,.2f}<extra></extra>",
    )
    fig_segment.update_layout(showlegend=False)
    style_chart(fig_segment, 470)

    st.markdown("**Sales Contribution by Customer Segment**")
    st.plotly_chart(fig_segment, use_container_width=True)

# =====================================================
# SHIPPING ANALYSIS
# =====================================================
st.markdown(
    '<div class="section-heading">Shipping Efficiency</div>',
    unsafe_allow_html=True,
)

shipping = filtered.dropna(
    subset=["order_date", "ship_date"]
).copy()

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

shipping_data["avg_shipping_days"] = (
    shipping_data["avg_shipping_days"].round(2)
)

fig_shipping = px.bar(
    shipping_data,
    x="ship_mode",
    y="avg_shipping_days",
    color="ship_mode",
    text="avg_shipping_days",
    color_discrete_sequence=[BLUE, TEAL, ORANGE, "#8B5CF6"],
    labels={
        "ship_mode": "Shipping Method",
        "avg_shipping_days": "Average Shipping Days",
    },
)
fig_shipping.update_traces(textposition="outside", cliponaxis=False)
fig_shipping.update_layout(showlegend=False)
style_chart(fig_shipping, 330)
st.plotly_chart(fig_shipping, use_container_width=True)


# =====================================================
# TOP 10 PRODUCT ANALYSIS
# =====================================================
import textwrap

st.markdown(
    '<div class="section-heading">Product Performance Analysis</div>',
    unsafe_allow_html=True,
)

product_data = (
    filtered.groupby(["product_id", "product_name"], as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum"),
        orders=("order_id", "nunique"),
    )
)

left, right = st.columns(2)


def wrap_product_name(name, width=27):
    """Wrap long product names for readable chart axis labels."""
    return "<br>".join(
        textwrap.wrap(str(name), width=width, break_long_words=False)
    )


# ---------------- TOP 10 PRODUCTS BY SALES ----------------
with left:
    top_sales = product_data.nlargest(10, "sales").sort_values("sales")

    fig_top_sales = px.bar(
        top_sales,
        x="sales",
        y="product_name",
        orientation="h",
        text="sales",
        color="sales",
        color_continuous_scale="Blues",
        custom_data=["profit", "quantity", "orders"],
        labels={
            "sales": "Sales ($)",
            "product_name": "Product",
            "color": "Sales",
        },
    )

    fig_top_sales.update_traces(
        texttemplate="$%{x:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Sales: $%{x:,.2f}<br>"
            "Profit: $%{customdata[0]:,.2f}<br>"
            "Units Sold: %{customdata[1]:,.0f}<br>"
            "Orders: %{customdata[2]}<extra></extra>"
        ),
    )

    style_chart(fig_top_sales, 600)

    fig_top_sales.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=10, r=65, t=20, b=55),
        bargap=0.30,
    )

    fig_top_sales.update_yaxes(
        tickmode="array",
        tickvals=top_sales["product_name"].tolist(),
        ticktext=[wrap_product_name(name) for name in top_sales["product_name"]],
        tickfont=dict(size=10),
        automargin=True,
        title_text="",
    )

    fig_top_sales.update_xaxes(
        title_text="Sales ($)",
        range=[0, max(top_sales["sales"].max() * 1.22, 1)],
    )

    st.markdown("**Top 10 Products by Sales**")
    st.plotly_chart(
        fig_top_sales,
        use_container_width=True,
        key="top_products_sales",
    )


# ---------------- TOP 10 PRODUCTS BY PROFIT ----------------
with right:
    top_profit = product_data.nlargest(10, "profit").sort_values("profit")

    fig_top_profit = px.bar(
        top_profit,
        x="profit",
        y="product_name",
        orientation="h",
        text="profit",
        color="profit",
        color_continuous_scale="Teal",
        custom_data=["sales", "quantity", "orders"],
        labels={
            "profit": "Profit ($)",
            "product_name": "Product",
            "color": "Profit",
        },
    )

    fig_top_profit.update_traces(
        texttemplate="$%{x:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Profit: $%{x:,.2f}<br>"
            "Sales: $%{customdata[0]:,.2f}<br>"
            "Units Sold: %{customdata[1]:,.0f}<br>"
            "Orders: %{customdata[2]}<extra></extra>"
        ),
    )

    style_chart(fig_top_profit, 600)

    fig_top_profit.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=10, r=65, t=20, b=55),
        bargap=0.30,
    )

    fig_top_profit.update_yaxes(
        tickmode="array",
        tickvals=top_profit["product_name"].tolist(),
        ticktext=[wrap_product_name(name) for name in top_profit["product_name"]],
        tickfont=dict(size=10),
        automargin=True,
        title_text="",
    )

    fig_top_profit.update_xaxes(
        title_text="Profit ($)",
        range=[0, max(top_profit["profit"].max() * 1.22, 1)],
    )

    st.markdown("**Top 10 Products by Profit**")
    st.plotly_chart(
        fig_top_profit,
        use_container_width=True,
        key="top_products_profit",
    )


# =====================================================
# DISCOUNT IMPACT ANALYSIS
# =====================================================
st.markdown(
    '<div class="section-heading">Discount & Profitability Analysis</div>',
    unsafe_allow_html=True,
)

discount_data = filtered.dropna(
    subset=["discount", "sales", "profit"]
).copy()

discount_data["discount_band"] = pd.cut(
    discount_data["discount"],
    bins=[-0.001, 0, 0.1, 0.2, 0.3, 0.5, 1.0],
    labels=[
        "No Discount",
        "1–10%",
        "11–20%",
        "21–30%",
        "31–50%",
        "Above 50%",
    ],
    include_lowest=True,
)

discount_summary = (
    discount_data.groupby("discount_band", observed=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        avg_discount=("discount", "mean"),
        records=("discount", "size"),
    )
    .reset_index()
)

discount_summary["profit_margin"] = (
    discount_summary["profit"]
    .div(discount_summary["sales"].replace(0, float("nan")))
    .mul(100)
)

left, right = st.columns(2)

with left:
    fig_discount_profit = px.bar(
        discount_summary,
        x="discount_band",
        y="profit",
        color="profit",
        color_continuous_scale="RdYlGn",
        text_auto=",.0f",
        hover_data=["sales", "records", "profit_margin"],
        labels={
            "discount_band": "Discount Range",
            "profit": "Total Profit ($)",
            "sales": "Sales ($)",
            "records": "Transaction Records",
            "profit_margin": "Profit Margin (%)",
        },
    )
    fig_discount_profit.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Discount Range",
        yaxis_title="Total Profit ($)",
    )
    style_chart(fig_discount_profit, 380)

    st.markdown("**Profit by Discount Range**")
    st.plotly_chart(fig_discount_profit, use_container_width=True)

with right:
    fig_discount_margin = px.bar(
        discount_summary,
        x="discount_band",
        y="profit_margin",
        color="profit_margin",
        color_continuous_scale="RdYlGn",
        text_auto=".1f",
        hover_data=["sales", "profit", "records"],
        labels={
            "discount_band": "Discount Range",
            "profit_margin": "Profit Margin (%)",
            "sales": "Sales ($)",
            "profit": "Profit ($)",
            "records": "Transaction Records",
        },
    )
    fig_discount_margin.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Discount Range",
        yaxis_title="Profit Margin (%)",
    )
    style_chart(fig_discount_margin, 380)

    st.markdown("**Profit Margin by Discount Range**")
    st.plotly_chart(fig_discount_margin, use_container_width=True)

st.caption(
    "Discount bands summarize transaction records. "
    "They show associations, not proof that discounts caused changes in profit."
)

# =====================================================
# BUSINESS INSIGHTS
# =====================================================
st.markdown(
    '<div class="section-heading">Quick Business Insights</div>',
    unsafe_allow_html=True,
)

best_category = category_data.loc[category_data["sales"].idxmax()]

region_data = df.groupby("region", as_index=False)["sales"].sum()
best_region = region_data.loc[region_data["sales"].idxmax()]

best_subcategory = subcategory_data.loc[subcategory_data["profit"].idxmax()]
worst_subcategory = subcategory_data.loc[subcategory_data["profit"].idxmin()]

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">LEADING CATEGORY BY SALES</div>
            <div class="insight-value">{best_category['category']}</div>
            <div style="color:{MUTED};font-size:12px;">
                ${best_category['sales']:,.0f} in sales
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i2:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">LEADING REGION BY SALES</div>
            <div class="insight-value">{best_region['region']}</div>
            <div style="color:{MUTED};font-size:12px;">
                ${best_region['sales']:,.0f} in sales
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i3:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">MOST PROFITABLE SUB-CATEGORY</div>
            <div class="insight-value">{best_subcategory['sub_category']}</div>
            <div style="color:{TEAL};font-size:12px;">
                ${best_subcategory['profit']:,.0f} profit
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i4:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">LOWEST-PROFIT SUB-CATEGORY</div>
            <div class="insight-value">{worst_subcategory['sub_category']}</div>
            <div style="color:{RED};font-size:12px;">
                ${worst_subcategory['profit']:,.0f} profit
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if worst_subcategory["profit"] < 0:
    st.warning(
        f"Review pricing, discounting, and costs for "
        f"{worst_subcategory['sub_category']}, which has the lowest "
        f"aggregate profit in the current selection. Investigate the "
        f"underlying transactions before deciding on corrective action."
    )

# =====================================================
# SEARCHABLE DATA TABLE
# =====================================================
st.markdown(
    '<div class="section-heading">Explore Order-Level Data</div>',
    unsafe_allow_html=True,
)

search = st.text_input(
    "Search orders, customers, or products",
    placeholder="Enter an order ID, customer name, or product...",
)

display_data = filtered.copy()

if search.strip():
    term = search.strip()
    mask = (
        display_data["order_id"].astype(str).str.contains(
            term, case=False, na=False
        )
        | display_data["customer_name"].astype(str).str.contains(
            term, case=False, na=False
        )
        | display_data["product_name"].astype(str).str.contains(
            term, case=False, na=False
        )
    )
    display_data = display_data[mask]

st.caption(f"{len(display_data):,} records match the current filters and search.")

# Render the preview as HTML so this section does not require PyArrow.
# Show a manageable preview; the CSV button below still downloads every matching row.
preview_rows = display_data.head(200)
table_html = preview_rows.to_html(index=False, escape=True, classes="retail-data-table")
st.markdown(
    f'<div class="retail-table-wrapper">{table_html}</div>',
    unsafe_allow_html=True,
)
if len(display_data) > len(preview_rows):
    st.caption(
        f"Showing the first {len(preview_rows):,} of {len(display_data):,} matching records. "
        "Download the CSV to access all matching records."
    )

st.download_button(
    "⬇ Download Filtered Data (CSV)",
    data=display_data.to_csv(index=False).encode("utf-8"),
    file_name="filtered_retail_sales.csv",
    mime="text/csv",
)

# =====================================================
# FOOTER
# =====================================================
st.markdown(
    """
    <div class="footer">
        RETAIL SALES & CUSTOMER INTELLIGENCE<br>
        Built with Python · SQL · Streamlit · Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
