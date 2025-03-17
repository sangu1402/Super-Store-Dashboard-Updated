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

# ---- Sidebar Date Range (From and To) ----
if df.empty:
    min_date, max_date = df_original["Order Date"].min(), df_original["Order Date"].max()
else:
    min_date, max_date = df["Order Date"].min(), df["Order Date"].max()

from_date = st.sidebar.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date)
to_date = st.sidebar.date_input("To Date", value=max_date, min_value=min_date, max_value=max_date)

if from_date > to_date:
    st.sidebar.error("From Date must be earlier than To Date.")

df = df[(df["Order Date"] >= pd.to_datetime(from_date)) & (df["Order Date"] <= pd.to_datetime(to_date))]

# ---- Page Title ----
st.title("SuperStore KPI Dashboard")

# ---- KPI Calculation ----
total_sales = df["Sales"].sum() if not df.empty else 0
total_quantity = df["Quantity"].sum() if not df.empty else 0
total_profit = df["Profit"].sum() if not df.empty else 0
margin_rate = (total_profit / total_sales) if total_sales != 0 else 0

# ---- KPI Percentage Change ----
df_previous = df_original[(df_original["Order Date"] >= pd.to_datetime(from_date) - pd.DateOffset(months=1)) & (df_original["Order Date"] < pd.to_datetime(from_date))]
previous_sales = df_previous["Sales"].sum() if not df_previous.empty else 0
sales_change = ((total_sales - previous_sales) / previous_sales * 100) if previous_sales != 0 else 0

# ---- KPI Display ----
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
with kpi_col1:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}", delta=f"{sales_change:.2f}%")
with kpi_col2:
    st.metric(label="Quantity Sold", value=f"{total_quantity:,}")
with kpi_col3:
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
with kpi_col4:
    st.metric(label="Margin Rate", value=f"{margin_rate*100:.2f}%")

# ---- Top 10 Products ----
st.subheader("Top 10 Products by Sales")
top_products = df.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
st.dataframe(top_products)

# ---- KPI Selection ----
st.subheader("Visualize KPI Across Time & Top Products")

if df.empty:
    st.warning("No data available for the selected filters and date range.")
else:
    kpi_options = ["Sales", "Quantity", "Profit", "Margin Rate"]
    selected_kpi = st.radio("Select KPI to display:", options=kpi_options, horizontal=True)

    daily_grouped = df.groupby("Order Date").agg({"Sales": "sum", "Quantity": "sum", "Profit": "sum"}).reset_index()
    daily_grouped["Margin Rate"] = daily_grouped["Profit"] / daily_grouped["Sales"].replace(0, 1)

    peak_date = daily_grouped.loc[daily_grouped[selected_kpi].idxmax(), "Order Date"]
    low_date = daily_grouped.loc[daily_grouped[selected_kpi].idxmin(), "Order Date"]

    fig_bar = px.bar(
        daily_grouped, x="Order Date", y=selected_kpi,
        title=f"{selected_kpi} Over Time", labels={"Order Date": "Date", selected_kpi: selected_kpi},
        template="plotly_white"
    )
    fig_bar.add_vline(x=peak_date.timestamp() * 1000, line_dash="dash", line_color="green", annotation_text="Peak")
    fig_bar.add_vline(x=low_date.timestamp() * 1000, line_dash="dash", line_color="red", annotation_text="Low")
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

    # ---- Pie Chart ----
    st.subheader("Sales Distribution by Category")
    category_sales = df.groupby("Category")["Sales"].sum().reset_index()
    fig_pie = px.pie(category_sales, names="Category", values="Sales", title="Sales by Category")
    st.plotly_chart(fig_pie, use_container_width=True)

    # ---- Download Filtered Data ----
    st.subheader("Download Filtered Data")
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="filtered_superstore_data.csv",
        mime="text/csv"
    )
