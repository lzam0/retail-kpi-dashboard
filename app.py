import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------------------------------
# Page Configuration
st.set_page_config(
    # Title and icon for the browser's tab bar:
    page_title="Retail KPI Dashboard",
    page_icon="🛍️",
    # Make the content take up the width of the page:
    layout="wide",
)

# ---------------------------------------------------------------------------
# Data Loading
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=['date'])
    # Calculate additional metrics
    df['net_revenue'] = df['sales_value'] - df['returns_value']
    df['atv'] = df['sales_value'] / df['purchases'].replace(0, np.nan)
    return df

df = load_data('retail_dataset.csv')

# ---------------------------------------------------------------------------
# Sidebar Filters
st.sidebar.header("Dashboard Filters")

# Date Range Filter
min_date = df['date'].min()
max_date = df['date'].max()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Channel Filter
channels = st.sidebar.multiselect(
    "Select Channel", 
    options=df['channel'].unique(), 
    default=list(df['channel'].unique())
)

# Promo & Holiday Toggles
show_promos_only = st.sidebar.checkbox("Show Promo Days Only")
show_holidays_only = st.sidebar.checkbox("Show Holidays Only")

# ---------------------------------------------------------------------------
# Filtering the dataframe
mask = (df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))
df_filtered = df.loc[mask]

if channels:
    df_filtered = df_filtered[df_filtered['channel'].isin(channels)]
if show_promos_only:
    df_filtered = df_filtered[df_filtered['promo_flag'] == 1]
if show_holidays_only:
    df_filtered = df_filtered[df_filtered['is_holiday'] == 1]

# ---------------------------------------------------------------------------
# Calculate KPIS
def calculate_kpi(df):
    total_footfall = df['footfall_or_sessions'].sum()
    total_purchase = df['purchases'].sum()
    total_returns = df['returns'].sum()
    total_sales_value = df['sales_value'].sum()
    total_returns_value = df['returns_value'].sum()
    revenue = total_sales_value - total_returns_value
    conversion_rate = total_purchase / total_footfall if total_footfall else 0

    return {
        'Footfall': total_footfall,
        'Purchases': total_purchase,
        'Returns': total_returns,
        'Sales': total_sales_value,
        'Returns Value': total_returns_value,
        'Revenue': revenue,
        'Conversion Rate': conversion_rate * 100
    }
kpis = calculate_kpi(df_filtered)

# ---------------------------------------------------------------------------
# Dashboard Content
st.title("Retail KPI Dashboard (Store + Online)")
st.markdown(f"**Data Period:** {start_date} to {end_date}")

left, right = st.columns([3, 2], gap="large")

# KPI display
with left.container(border=True):
    st.markdown(f"### Executive Summary ({df['date'].dt.year.max()})")

    r1c1, r1c2, r1c3 = st.columns(3)
    r1c1.metric("Footfall", f"{kpis['Footfall']:,}")
    r1c2.metric("Purchases", f"{kpis['Purchases']:,}")
    r1c3.metric("Returns", f"{kpis['Returns']:,}")

    r2c1, r2c2 = st.columns(2)
    r2c1.metric("Sales", f"£{kpis['Sales']:,}")
    r2c2.metric("Returns Value", f"£{kpis['Returns Value']:,}")

    r3c1, r3c2 = st.columns(2)
    r3c1.metric("Revenue", f"£{kpis['Revenue']:,}")
    r3c2.metric("Conversion Rate", f"{kpis['Conversion Rate']:.2f}%")

# ---------------------------------------------------------------------------
# Weekly KPI vs Last Week
df_weekly = df_filtered.copy()
df_weekly['week'] = df_weekly['date'].dt.isocalendar().week
df_weekly['year'] = df_weekly['date'].dt.year

current_year = df_weekly['year'].max()
current_week = df_weekly[df_weekly['year'] == current_year]['week'].max()
last_week = current_week - 1

this_week_df = df_weekly[
    (df_weekly['year'] == current_year) &
    (df_weekly['week'] == current_week)
]

last_week_df = df_weekly[
    (df_weekly['year'] == current_year) &
    (df_weekly['week'] == last_week)
]

this_week_kpis = calculate_kpi(this_week_df)
last_week_kpis = calculate_kpi(last_week_df)

def pct_change(current, previous):
    if previous == 0:
        return None
    return ((current - previous) / previous) * 100

with right.container(border=True):
    st.markdown(f"### Weekly Performance")
    st.caption(f"Week {current_week} vs Week {last_week}")

    st.metric(
        "Revenue",
        f"£{this_week_kpis['Revenue']:,}",
        f"{pct_change(this_week_kpis['Revenue'], last_week_kpis['Revenue']):.1f}%"
        if last_week_kpis['Revenue'] else "N/A"
    )

    st.metric(
        "Purchases",
        f"{this_week_kpis['Purchases']:,}",
        f"{pct_change(this_week_kpis['Purchases'], last_week_kpis['Purchases']):.1f}%"
        if last_week_kpis['Purchases'] else "N/A"
    )

    st.metric(
        "Footfall",
        f"{this_week_kpis['Footfall']:,}",
        f"{pct_change(this_week_kpis['Footfall'], last_week_kpis['Footfall']):.1f}%"
        if last_week_kpis['Footfall'] else "N/A"
    )

    st.metric(
        "Conversion Rate",
        f"{this_week_kpis['Conversion Rate']:.2f}%",
        f"{pct_change(this_week_kpis['Conversion Rate'], last_week_kpis['Conversion Rate']):.1f}%"
        if last_week_kpis['Conversion Rate'] else "N/A"
    )
# ---------------------------------------------------------------------------
# Monthly Sales
df_filtered['month'] = df_filtered['date'].dt.month_name()

months_order = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
]

monthly_sales = (
    df_filtered.groupby('month')['sales_value']
    .sum()
    .reindex(months_order)
    .reset_index()
)

fig_tree = px.treemap(
    monthly_sales,
    path=['month'],
    values='sales_value',
    color='sales_value',
    color_continuous_scale='Viridis',
    title="Sales Contribution by Month"
)

st.plotly_chart(fig_tree, use_container_width=True)

# ---------------------------------------------------------------------------
# Daily Trends
st.subheader("Sales & Conversion Trends")
daily = df_filtered.groupby('date').sum().reset_index()
daily['Conversion Rate'] = daily['purchases'] / daily['footfall_or_sessions'] * 100

fig_sales = px.line(daily, x='date', y='sales_value', title='Daily Sales (£)')
fig_conv = px.line(daily, x='date', y='Conversion Rate', title='Daily Conversion Rate (%)')

st.plotly_chart(fig_sales)
st.plotly_chart(fig_conv)

