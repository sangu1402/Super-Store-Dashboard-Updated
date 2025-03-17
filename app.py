import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Load or Generate Sample Data
data = {
    'Month': pd.date_range(start='2023-01-01', periods=12, freq='M').strftime('%b'),
    'Receivables': [6000, 6200, 5900, 5800, 6100, 6300, 6500, 6700, 6800, 6900, 7000, 7100],
    'Payables': [2000, 2100, 2200, 1900, 2000, 2300, 2400, 2500, 2600, 2700, 2800, 2900],
    'Equity Ratio': [75.5, 76.2, 74.8, 75.9, 76.5, 77.0, 76.8, 76.9, 77.2, 77.5, 78.0, 78.2],
    'Debt Equity': [1.1, 1.2, 1.1, 1.0, 1.1, 1.3, 1.4, 1.2, 1.3, 1.2, 1.1, 1.0]
}
df = pd.DataFrame(data)

# Streamlit Layout
st.set_page_config(layout='wide', page_title='Financial Dashboard')
st.title("📊 Financial Dashboard")

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Receivables", f"${df['Receivables'].sum():,.0f}")
col2.metric("Total Payables", f"${df['Payables'].sum():,.0f}", "-5%")
col3.metric("Equity Ratio", f"{df['Equity Ratio'].mean():.2f}%")
col4.metric("Debt Equity", f"{df['Debt Equity'].mean():.2f}")

# Line Chart: Net Working Capital
df['Net Working Capital'] = df['Receivables'] - df['Payables']
fig1 = px.line(df, x='Month', y='Net Working Capital', title='Net Working Capital Over Time')
st.plotly_chart(fig1, use_container_width=True)

# Bar Chart: Receivables vs Payables
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=df['Month'], y=df['Receivables'], name='Receivables'))
fig2.add_trace(go.Bar(x=df['Month'], y=df['Payables'], name='Payables'))
fig2.update_layout(barmode='group', title='Receivables vs Payables by Month')
st.plotly_chart(fig2, use_container_width=True)

# Profit and Loss Summary
fig3 = px.bar(df, x='Month', y=['Receivables', 'Payables'], title='Profit and Loss Summary', barmode='stack')
st.plotly_chart(fig3, use_container_width=True)

# Sidebar Filters
st.sidebar.header("Filters")
selected_months = st.sidebar.multiselect("Select Months", df['Month'].unique(), df['Month'].unique())
df_filtered = df[df['Month'].isin(selected_months)]

# Display Filtered Data
tab1, tab2 = st.tabs(["📊 Data", "📈 Charts"])
with tab1:
    st.dataframe(df_filtered)
with tab2:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

st.caption("Designed using Streamlit & Plotly")
