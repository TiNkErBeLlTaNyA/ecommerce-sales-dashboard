import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===== PAGE CONFIG =====
st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")

# ===== DASHBOARD TITLE =====
st.title("E-Commerce Sales Dashboard")
st.caption("Professional dashboard for e-commerce sales insights")

# ===== LOAD DATA =====
df = pd.read_csv("sales_data.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Revenue"] = df["Quantity"] * df["Price"]

# ===== SIDEBAR FILTERS =====
st.sidebar.header("Filters")

# Date Range
min_date = df["OrderDate"].min()
max_date = df["OrderDate"].max()
date_filter = st.sidebar.date_input(
    "Select Date Range", value=(min_date, max_date)
)

# Category
category_filter = st.sidebar.selectbox(
    "Select Category", options=["All"] + list(df["Category"].unique())
)

# Region
region_filter = st.sidebar.selectbox(
    "Select Region", options=["All"] + list(df["Region"].unique())
)

# ===== APPLY FILTERS =====
filtered_df = df[
    (df["OrderDate"] >= pd.to_datetime(date_filter[0])) &
    (df["OrderDate"] <= pd.to_datetime(date_filter[1]))
]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]
if region_filter != "All":
    filtered_df = filtered_df[filtered_df["Region"] == region_filter]

# ===== KPIs =====
total_sales = filtered_df["Revenue"].sum()
total_orders = filtered_df["OrderID"].nunique()
top_product = (
    filtered_df.groupby("Product")["Revenue"].sum().idxmax()
    if not filtered_df.empty else "No data"
)

# --- KPI COLUMNS ---
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_sales}")
col2.metric("Total Orders", total_orders)

# Highlight top product with a subtle style
col3.markdown(
    f"<div style='padding:10px; background-color:#F3F4F6; border-radius:8px; text-align:center;'>"
    f"<h4>Top Product</h4><h3>{top_product}</h3></div>",
    unsafe_allow_html=True
)

st.divider()

# ===== CHARTS =====
col_left, col_right = st.columns(2)

# Category Sales
with col_left:
    st.subheader("Revenue by Category")
    category_sales = filtered_df.groupby("Category")["Revenue"].sum()
    fig1, ax1 = plt.subplots(figsize=(4,2.5))
    category_sales.plot(kind="bar", ax=ax1, color="#2563EB")
    ax1.set_ylabel("Revenue")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig1)

# Region Sales
with col_right:
    st.subheader("Revenue by Region")
    region_sales = filtered_df.groupby("Region")["Revenue"].sum()
    fig2, ax2 = plt.subplots(figsize=(4,2.5))
    region_sales.plot(kind="barh", ax=ax2, color="#10B981")
    ax2.set_xlabel("Revenue")
    ax2.grid(axis="x", linestyle="--", alpha=0.3)
    st.pyplot(fig2)

# Monthly Trend
with st.expander("Monthly Revenue Trend"):
    trend_df = filtered_df.copy()
    trend_df["Month"] = trend_df["OrderDate"].dt.to_period("M")
    monthly_sales = trend_df.groupby("Month")["Revenue"].sum()
    fig3, ax3 = plt.subplots(figsize=(7,2.8))
    monthly_sales.plot(ax=ax3, marker="o", color="#111827")
    ax3.set_ylabel("Revenue")
    ax3.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig3)

# ===== DOWNLOAD BUTTON =====
st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# ===== FOOTER =====
st.markdown("---")
st.caption("Dashboard built using Python, Pandas, Matplotlib & Streamlit")
