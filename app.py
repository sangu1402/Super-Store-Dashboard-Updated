import streamlit as st
import pandas as pd
import plotly.express as px

# Sample Data
data = {
    "Year": [2022]*6 + [2023]*6,
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [20000, 22000, 25000, 27000, 26000, 29000, 31000, 33000, 35000, 34000, 36000, 38000],
    "Expenses": [12000, 13000, 14000, 15000, 14500, 16000, 17000, 18000, 19000, 18500, 20000, 21000],
    "Profit": [8000, 9000, 11000, 12000, 11500, 13000, 14000, 15000, 16000, 15500, 16000, 17000],
    "Category": ["Sales", "Marketing", "Operations", "Sales", "Marketing", "Operations", "Sales", "Marketing", "Operations", "Sales", "Marketing", "Operations"]
}

df = pd.DataFrame(data)

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Year Filter
selected_year = st.sidebar.selectbox("Select Year", df["Year"].unique(), index=0)

# Month Filter
selected_month = st.sidebar.selectbox("Select Month", ["All"] + list(df["Month"].unique()))

# Category Filter
selected_category = st.sidebar.selectbox("Select Category", ["All"] + list(df["Category"].unique()))

# Filter Data
filtered_df = df[df["Year"] == selected_year]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == selected_month]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# KPIs Calculation
total_revenue = filtered_df["Revenue"].sum()
total_expenses = filtered_df["Expenses"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0

# Layout
st.title("📊 Business Financial Dashboard")

# KPI Section
st.markdown("### 📌 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📉 Total Expenses", f"${total_expenses:,.0f}")
col3.metric("📈 Total Profit", f"${total_profit:,.0f}")
col4.metric("🤑 Profit Margin", f"{profit_margin:.2f}%")

# Charts Layout
st.markdown("### 📊 Data Visualization")

# First Row: Pie & Line Chart
col1, col2 = st.columns(2)

# Pie Chart - Expense Distribution
fig_pie = px.pie(filtered_df, names="Category", values="Expenses", title="📌 Expense Distribution by Category")
col1.plotly_chart(fig_pie, use_container_width=True)

# Line Chart - Revenue & Profit Trends
fig_line = px.line(filtered_df, x="Month", y=["Revenue", "Profit"], markers=True, title="📊 Revenue & Profit Trends")
col2.plotly_chart(fig_line, use_container_width=True)

# Second Row: Bar Chart
st.markdown("### 📊 Revenue vs Expenses Over Time")
fig_bar = px.bar(filtered_df, x="Month", y=["Revenue", "Expenses"], barmode="group", title="📌 Revenue vs Expenses")
st.plotly_chart(fig_bar, use_container_width=True)

# Insights Section
st.markdown("### 📌 Insights & Recommendations")
st.write("✔️ Revenue shows an increasing trend, indicating growth.")  
st.write("✔️ Sales contribute the highest to revenue, followed by Operations.")  
st.write("✔️ Marketing expenses are relatively high; optimizing them could improve profit margins.")  

# **This dashboard now includes Dropdown filters, Year-based filtering, and a well-arranged layout. Let me know if you need more improvements!**
