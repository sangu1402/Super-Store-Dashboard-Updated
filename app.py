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

df = df_filtered_state.copy()

# ---- Page Title ----
st.title("SuperStore KPI Dashboard")

# ---- KPI Calculation ----
total_sales = df["Sales"].sum() if not df.empty else 0
total_expenses = df["Profit"].sum() if not df.empty else 0  # Placeholder for expenses

# ---- Pie Chart & Bar Chart Side-by-Side ----
st.subheader("Sales and Expenses Overview")

col1, col2 = st.columns(2)

with col1:
    category_sales = df.groupby("Category")["Sales"].sum().reset_index()
    fig_pie = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales Breakdown by Category",
        hole=0.3,
        template="plotly_white"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    revenue_expenses_df = pd.DataFrame({
        "Category": ["Revenue", "Expenses"],
        "Amount": [total_sales, total_expenses]
    })
    fig_bar = px.bar(
        revenue_expenses_df,
        x="Category",
        y="Amount",
        title="Revenue vs Expenses",
        color="Category",
        text_auto=True,
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
