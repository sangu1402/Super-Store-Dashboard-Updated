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
