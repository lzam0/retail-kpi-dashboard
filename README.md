# Retail KPI Dashboard (Store & Online)

## Project Overview
This project is a **Retail Performance KPI Dashboard** designed to help retail managers monitor and analyse the performance of both physical stores and online channels. The dashboard tracks **daily and weekly KPIs** such as traffic, sales, conversion, and returns, providing actionable insights to support operational and strategic decision-making.

The project is inspired by real-world retail operations (e.g., Nike), where metrics like footfall, purchases, online sales, and returns are critical for understanding business performance.

---

## Objectives
- Track key performance indicators (KPIs) for **store and online sales**.
- Compare **daily, weekly, monthly and even yearly trends** across channels.
- Identify bottlenecks and opportunities in **conversion and sales**.
- Generate actionable insights for management decisions.

---

## Key Performance Indicators (KPIs)

### Traffic
- **Store Footfall:** Number of customers entering the store daily.
- **Online Sessions:** Number of visits to the online store.

### Sales
- **Store Sales (£)**
- **Online Sales (£)**
- **Total Revenue (£)**
- **Average Transaction Value (£)**

### Conversion
- **Store Conversion Rate:** Purchases ÷ Footfall
- **Online Conversion Rate:** Orders ÷ Sessions

### Returns
- **Number of Returns (Store & Online)**
- **Return Rate:** Returns ÷ Purchases
- **Return Value (£)**
- **Net Revenue (£):** Total Revenue – Return Value

### Growth Metrics
- **Daily Change (%)**
- **Week-over-Week Change (%)**
- **Channel Contribution:** Store vs Online revenue

---

## Dashboard Layout

### 1. Executive Summary
Top-level KPI cards showing:
- Today vs yesterday values
- Daily and weekly % change
- Quick-glance overview for managers

### 2. Channel Performance
- Store vs Online revenue comparison
- Conversion rates per channel

### 3. Trends
- Daily sales trends (line chart)
- Weekly revenue trends
- Returns trends over time

### 4. Funnel Analysis
**Store Funnel:** Footfall → Purchases  
**Online Funnel:** Sessions → Add to Cart → Checkout → Purchase  

Highlights drop-offs and conversion bottlenecks.

### 5. Insights Panel
Automated, analyst-style insights such as:
> “Online revenue increased 12% WoW due to improved conversion, while store footfall declined 5%, impacting overall revenue growth.”

---

## Tools & Technologies
- **Python** – Data cleaning and KPI calculations
- **Pandas & NumPy** – Data manipulation
- **Matplotlib & Plotly** – Visualization
- **Streamlit** – Interactive dashboard deployment
- **Jupyter Notebook** – KPI exploration and prototyping

---

## Dataset
The dataset is **synthetic but realistic**, designed to mimic real-world retail operations:
- `date`: Daily timestamps
- `channel`: `store` or `online`
- `footfall_or_sessions`: Daily traffic
- `purchases`: Number of purchases
- `returns`: Number of returns
- `sales_value`: Total revenue
- `returns_value`: Total value of returns
- Optional: `weekday`, `promo_flag`

This dataset allows for realistic **daily and weekly KPI tracking**, similar to metrics used in large retail chains.

---

## Insights & Use Cases
- Quickly identify **drops in conversion** to prioritise operational fixes.
- Understand **channel contribution**, e.g., whether online is complementing or cannibalising store sales.
- Track **weekly trends** to support management decisions.
- Analyse **returns impact** on net revenue to optimise return policies.

---

## Future Improvements
- Add **forecasting** for footfall and sales using time-series models.
- Implement **alerts** for KPIs falling below threshold values.
- Segment by **store location, region, or product category**.
- Integrate **promotions and campaigns** to measure impact on conversion.

---

## How to Run
1. Install required packages:
```bash
pip install pandas numpy matplotlib plotly streamlit
