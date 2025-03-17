import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Sample data generation
data = {
    'Month': pd.date_range(start='1/1/2023', periods=12, freq='M').strftime('%b'),
    'Accounts_Receivable': np.random.randint(5000, 20000, 12),
    'Accounts_Payable': np.random.randint(2000, 10000, 12),
    'Equity_Ratio': np.random.uniform(50, 90, 12),
    'Debt_Equity': np.random.uniform(0.5, 2.5, 12)
}
df = pd.DataFrame(data)

# Streamlit UI
st.set_page_config(layout="wide", page_title="Financial Dashboard")
st.title("📊 Financial Dashboard")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Accounts Receivable", f"${df['Accounts_Receivable'].sum():,.0f}")
col2.metric("Total Accounts Payable", f"${df['Accounts_Payable'].sum():,.0f}", "-10%")
col3.metric("Equity Ratio", f"{df['Equity_Ratio'].mean():.2f}%")
col4.metric("Debt Equity", f"{df['Debt_Equity'].mean():.2f}")

# Charts
st.subheader("📈 Financial Performance Over Time")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(x='Month', y='Accounts_Receivable', data=df, marker='o', label='Receivable', ax=ax1)
sns.lineplot(x='Month', y='Accounts_Payable', data=df, marker='o', label='Payable', ax=ax1)
ax1.set_ylabel("Amount ($)")
ax1.set_title("Accounts Receivable & Payable Trend")
st.pyplot(fig1)

st.subheader("📊 Accounts Breakdown")
fig2 = px.bar(df, x='Month', y=['Accounts_Receivable', 'Accounts_Payable'], 
              barmode='group', title="Monthly Accounts Overview")
st.plotly_chart(fig2, use_container_width=True)

# Add a filter for interactivity
st.sidebar.header("🔍 Filter Data")
selected_month = st.sidebar.selectbox("Select Month", df['Month'])
filtered_data = df[df['Month'] == selected_month]
st.sidebar.write("### Selected Month Data", filtered_data)

st.success("Dashboard successfully loaded! 🚀")
