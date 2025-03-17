!pip install seaborn -q
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Set Streamlit page configuration
st.set_page_config(page_title="SuperStore Sales Dashboard", layout="wide")

# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_excel("Sample - Superstore.xlsx", engine="openpyxl")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df_original = load_data()

# ---- Sidebar Filters ----
st.sidebar.header("Filter Data")

# Multi-select filters
selected_region = st.sidebar.multiselect("Select Region", df_original["Region"].unique(), default=df_original["Region"].unique())
selected_state = st.sidebar.multiselect("Select State", df_original["State"].unique(), default=df_original["State"].unique())
selected_category = st.sidebar.multiselect("Select Category", df_original["Category"].unique(), default=df_original["Category"].unique())

# Date range filter
min_date, max_date = df_original["Order Date"].min(), df_original["Order Date"].max()
from_date = st.sidebar.date_input("From Date", min_date, min_value=min_date, max_value=max_date)
to_date = st.sidebar.date_input("To Date", max_date, min_value=min_date, max_value=max_date)

# Apply filters
df = df_original[
    (df_original["Region"].isin(selected_region)) &
    (df_original["State"].isin(selected_state)) &
    (df_original["Category"].isin(selected_category)) &
    (df_original["Order Date"] >= pd.to_datetime(from_date)) &
    (df_original["Order Date"] <= pd.to_datetime(to_date))
]

# ---- Main Tabs ----
tab1, tab2, tab3 = st.tabs(["📊 Dashboard Overview", "📈 Sales Analysis", "🛍️ Customer Insights"])

# ---- Tab 1: Dashboard Overview ----
with tab1:
    st.title("📊 SuperStore Sales Dashboard")
    
    # KPI Metrics
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    margin_rate = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Orders", f"{total_orders:,}")
    col4.metric("Margin Rate", f"{margin_rate:.2f}%")

    # Sales Trend Line Chart
    sales_trend = df.groupby("Order Date")["Sales"].sum().reset_index()
    fig_trend = px.line(sales_trend, x="Order Date", y="Sales", title="Sales Trend Over Time", template="plotly_white")
    st.plotly_chart(fig_trend, use_container_width=True)

# ---- Tab 2: Sales Analysis ----
with tab2:
    st.header("📈 Sales & Profit Analysis")

    # Sales by Region (Map)
    sales_by_region = df.groupby("State")["Sales"].sum().reset_index()
    fig_map = px.choropleth(
        sales_by_region,
        locations="State",
        locationmode="USA-states",
        color="Sales",
        scope="usa",
        title="Sales by State",
        color_continuous_scale="blues"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col5, col6 = st.columns(2)

    with col5:
        # Sales Distribution Pie Chart
        category_sales = df.groupby("Category")["Sales"].sum().reset_index()
        fig_pie = px.pie(category_sales, names="Category", values="Sales", title="Sales Breakdown by Category", hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col6:
        # Profitability by Sub-Category (Bar Chart)
        subcategory_profit = df.groupby("Sub-Category")["Profit"].sum().reset_index()
        subcategory_profit = subcategory_profit.sort_values(by="Profit", ascending=False)
        fig_bar = px.bar(subcategory_profit, x="Profit", y="Sub-Category", orientation="h", title="Profitability by Sub-Category", color="Profit")
        st.plotly_chart(fig_bar, use_container_width=True)

# ---- Tab 3: Customer Insights ----
with tab3:
    st.header("🛍️ Customer Insights")

    # Top 5 High-Spending Customers
    top_customers = df.groupby("Customer Name")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(5)
    st.subheader("🏆 Top 5 High-Spending Customers")
    st.table(top_customers)

    # Order Frequency Heatmap
    df["Order Month"] = df["Order Date"].dt.strftime("%Y-%m")
    order_heatmap = df.groupby(["Order Month", "Region"])["Order ID"].count().unstack()

    st.subheader("📅 Order Frequency Heatmap")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(order_heatmap, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
    st.pyplot(fig)

# ---- Footer ----
st.markdown("---")
st.markdown("🔹 **SuperStore Sales Dashboard** | Created with ❤️ using Streamlit & Plotly")
