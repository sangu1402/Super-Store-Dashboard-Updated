import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", parse_dates=["Order Date", "Ship Date"])
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
kpi_options = ["Sales", "Profit", "Quantity"]
selected_kpi = st.sidebar.selectbox("Select KPI", kpi_options)

# KPI metric
st.metric(label=f"Total {selected_kpi}", value=f"{df[selected_kpi].sum():,.2f}")

# Prepare data

daily_grouped = df.groupby("Order Date")[selected_kpi].sum().reset_index()
top_10 = df.groupby("Product Name")[selected_kpi].sum().nlargest(10).reset_index()
category_sales = df.groupby("Category")["Sales"].sum().reset_index()

# Layout
col1, col2 = st.columns([2, 1])
col_left, col_right = st.columns(2)

# CSS for borders
st.markdown(
    """
    <style>
    .chart-box {
        border: 2px solid #EAEAEA;
        border-radius: 8px;
        padding: 16px;
        margin: 8px;
        background-color: #FFFFFF;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Line Chart
with col_left:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    fig_line = px.line(daily_grouped, x="Order Date", y=selected_kpi, 
                       title=f"{selected_kpi} Over Time", template="plotly_white")
    fig_line.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20), 
                           plot_bgcolor="white", paper_bgcolor="white", 
                           xaxis=dict(showgrid=False), yaxis=dict(showgrid=True))
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Bar Chart
with col_right:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    fig_bar = px.bar(top_10, x=selected_kpi, y="Product Name", 
                     orientation="h", title=f"Top 10 Products by {selected_kpi}", 
                     color=selected_kpi, template="plotly_white")
    fig_bar.update_traces(texttemplate='%{x:.2s}', textposition='outside')
    fig_bar.update_layout(margin=dict(l=20, r=20, t=50, b=20), 
                          plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Pie Chart
with col2:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    fig_pie = px.pie(category_sales, names="Category", values="Sales", 
                     title="Sales Breakdown by Category", hole=0.3, template="plotly_white")
    fig_pie.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
