import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

DB_PATH = "/Users/bliu/LearningProjects/brokerage-kpi/brokerage.duckdb"

st.set_page_config(page_title="Brokerage KPI Dashboard", layout="wide")
st.title("Brokerage Analytics Dashboard")
st.markdown("Built with Python, dbt, DuckDB, and Streamlit")

@st.cache_data
def load_data():
    # for duckdb
    '''conn = duckdb.connect(DB_PATH, read_only=True)
    daily = conn.execute("SELECT * FROM fct_daily_active_traders ORDER BY trade_date").df()
    volume = conn.execute("SELECT * FROM fct_volume_by_ticker ORDER BY month").df()
    users = conn.execute("SELECT * FROM fct_user_metrics ORDER BY total_volume DESC").df()
    conn.close()'''
    # for streamlit deploy
    daily = pd.read_csv("data/exports/fct_daily_active_traders.csv")
    volume = pd.read_csv("data/exports/fct_volume_by_ticker.csv")
    users = pd.read_csv("data/exports/fct_user_metrics.csv")
    return daily, volume, users

daily, volume, users = load_data()

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", f"{len(users):,}")
col2.metric("Total Trades", f"{daily['total_trades'].sum():,}")
col3.metric("Total Volume", f"${users['total_volume'].sum():,.0f}")
col4.metric("Avg Retention Rate", f"{users['retention_rate'].mean():.1f}%")

st.divider()

# --- Daily Active Traders ---
st.subheader("Daily Active Traders")
fig1 = px.line(daily, x="trade_date", y="daily_active_traders")
st.plotly_chart(fig1, use_container_width=True)

# --- Volume by Ticker ---
st.subheader("Monthly Volume by Ticker")
fig2 = px.bar(volume, x="month", y="total_volume", color="ticker", barmode="stack")
st.plotly_chart(fig2, use_container_width=True)

# --- Buy vs Sell by Ticker ---
st.subheader("Buy vs Sell Volume by Ticker")
ticker_summary = volume.groupby("ticker")[["buy_volume", "sell_volume"]].sum().reset_index()
fig3 = px.bar(ticker_summary, x="ticker", y=["buy_volume", "sell_volume"], barmode="group")
st.plotly_chart(fig3, use_container_width=True)

# --- Top Users by Volume ---
st.subheader("Top 20 Users by Trading Volume")
top_users = users.head(20)
fig4 = px.bar(top_users, x="user_id", y="total_volume", color="account_type")
st.plotly_chart(fig4, use_container_width=True)

# --- Retention by Account Type ---
st.subheader("Retention Rate by Account Type")
retention = users.groupby("account_type")["retention_rate"].mean().reset_index()
fig5 = px.bar(retention, x="account_type", y="retention_rate", color="account_type",
              title="Average Monthly Retention Rate (%)")
st.plotly_chart(fig5, use_container_width=True)

# --- Volume by Country ---
st.subheader("Trading Volume by Country")
country = users.groupby("country")["total_volume"].sum().reset_index()
fig6 = px.pie(country, names="country", values="total_volume")
st.plotly_chart(fig6, use_container_width=True)
