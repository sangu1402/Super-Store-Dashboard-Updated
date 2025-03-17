import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page config for wide layout
st.set_page_config(page_title="SuperStore KPI Dashboard", layout="wide")

# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_excel("Sample - Superstore.xlsx", engine="openpyxl")
    if not pd.api.types.is_datetime64_any_dtype(df["Order Date"]):
        df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df_original = load_data()

# ---- Sidebar Filters ----
st.sidebar.title("Filters")

all_regions = sorted(df_original["Region"].dropna().unique())
selected_region = st.sidebar.selectbox("Select Region", options=["All"] + all_regions)

df_filtered_region = df_original if selected_region == "All" else df_original[df_original["Region"] == selected_region]

all_states = sorted(df_filtered_region["State"].dropna().unique())
selected_state = st.sidebar.selectbox("Select State", options=["All"] + all_states)

df_filtered_state = df_filtered_region if selected_state == "All" else df_filtered_region[df_filtered_region["State"] == selected_state]

all_categories = sorted(df_filtered_state["Category"].dropna().unique())
selected_category = st.sidebar.selectbox("Select Category", options=["All"] + all_categories)

df_filtered_category = df_filtered_state if selected_category == "All" else df_filtered_state[df_filtered_state["Category"] == selected_category]

all_subcats = sorted(df_filtered_category["Sub-Category"].dropna().unique())
selected_subcat = st.sidebar.selectbox("Select Sub-Category", options=["All"] + all_subcats)

df = df_filtered_category if selected_subcat == "All" else df_filtered_category[df_filtered_category["Sub-Category"] == selected_subcat]

if df.empty:
    min_date, max_date = df_original["Order Date"].min(), df_original["Order Date"].max()
else:
    min_date, max_date = df["Order Date"].min(), df["Order Date"].max()

from_date = st.sidebar.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date)
to_date = st.sidebar.date_input("To Date", value=max_date, min_value=min_date, max_value=max_date)

if from_date > to_date:
    st.sidebar.error("From Date must be earlier than To Date.")

df = df[(df["Order Date"] >= pd.to_datetime(from_date)) & (df["Order Date"] <= pd.to_datetime(to_date))]

st.title("SuperStore KPI Dashboard")

if df.empty:
    total_sales, total_quantity, total_profit, margin_rate = 0, 0, 0, 0
else:
    total_sales, total_quantity, total_profit = df["Sales"].sum(), df["Quantity"].sum(), df["Profit"].sum()
    margin_rate = (total_profit / total_sales) if total_sales != 0 else 0

st.subheader("Visualize KPI Across Time & Top Products")

if df.empty:
    st.warning("No data available for the selected filters and date range.")
else:
    kpi_options = ["Sales", "Quantity", "Profit", "Margin Rate"]
    selected_kpi = st.radio("Select KPI to display:", options=kpi_options, horizontal=True)

    daily_grouped = df.groupby("Order Date").agg({"Sales": "sum", "Quantity": "sum", "Profit": "sum"}).reset_index()
    daily_grouped["Margin Rate"] = daily_grouped["Profit"] / daily_grouped["Sales"].replace(0, 1)

    product_grouped = df.groupby("Product Name").agg({"Sales": "sum", "Quantity": "sum", "Profit": "sum"}).reset_index()
    product_grouped["Margin Rate"] = product_grouped["Profit"] / product_grouped["Sales"].replace(0, 1)
    product_grouped.sort_values(by=selected_kpi, ascending=False, inplace=True)
    top_10 = product_grouped.head(10)

    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_line = px.line(daily_grouped, x="Order Date", y=selected_kpi, title=f"{selected_kpi} Over Time", template="plotly_white")
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col_right:
        fig_bar = px.bar(top_10, x=selected_kpi, y="Product Name", orientation="h", title=f"Top 10 Products by {selected_kpi}", template="plotly_white")
        fig_bar.update_traces(texttemplate='%{x:.2s}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Sales Distribution by Category")
category_sales = df.groupby("Category")["Sales"].sum().reset_index()

col1, col2 = st.columns([1, 1])

with col1:
    fig_pie = px.pie(category_sales, names="Category", values="Sales", title="Sales Breakdown by Category", hole=0.3, template="plotly_white")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    revenue_expense_data = pd.DataFrame({
        "Metric": ["Revenue", "Expenses"],
        "Value": [df["Sales"].sum(), df["Sales"].sum() - df["Profit"].sum()]
    })
    fig_revenue_expense = px.bar(revenue_expense_data, x="Metric", y="Value", title="Revenue vs Expenses", text_auto=True, template="plotly_white")
    st.plotly_chart(fig_revenue_expense, use_container_width=True)
