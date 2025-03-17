import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data (Replace with your dataset)
data = pd.read_csv("your_dataset.csv")

# Sidebar for Filters
st.sidebar.title("Filters")
category = st.sidebar.selectbox("Select Category", data['Category'].unique())
filtered_data = data[data['Category'] == category]

# Main Dashboard Layout
st.title("📊 Business Dashboard")
st.markdown("---")

# KPI Section
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_data['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_data['Profit'].sum():,.2f}")
col3.metric("Orders", f"{filtered_data.shape[0]}")

# Sales Trend Over Time
st.subheader("Sales Trend")
fig, ax = plt.subplots()
filtered_data.groupby('Order Date')['Sales'].sum().plot(ax=ax)
ax.set_ylabel("Sales")
ax.set_xlabel("Date")
st.pyplot(fig)

# Category-wise Sales
st.subheader("Sales by Sub-Category")
fig, ax = plt.subplots()
sns.barplot(x='Sales', y='Sub-Category', data=filtered_data, ax=ax)
st.pyplot(fig)

# Customer Segment Analysis
st.subheader("Customer Segment Distribution")
fig, ax = plt.subplots()
filtered_data['Segment'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
st.pyplot(fig)

st.markdown("---")
st.write("Dashboard created by [Your Name]")
