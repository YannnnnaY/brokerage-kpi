# Brokerage KPI Analytics Pipeline

An end-to-end analytics engineering project simulating a real brokerage data platform. Generates synthetic trading data, models it through a multi-layer dbt pipeline, and serves business KPIs via an interactive dashboard.

## Live Demo
[View Live Dashboard](https://brokerage-kpi-wcnemmsrqjqnutgebttney.streamlit.app)

---

## Architecture

```
Synthetic Data Generator (Python + Faker)
  • 1,000 users
  • 50,000 trades
  • 8 instruments
       │
       ▼
DuckDB Data Warehouse
  • raw_users
  • raw_trades
  • raw_instruments
       │
       ▼
dbt Transformation Layers
  ├── Staging:      stg_users, stg_trades, stg_instruments
  ├── Intermediate: int_user_trade_summary, int_monthly_retention
  └── Marts:        fct_daily_active_traders, fct_volume_by_ticker, fct_user_metrics
       │
       ▼
Streamlit Dashboard (Plotly charts)
```

---

## Data Model Design

The data model follows a layered analytics engineering approach:

- **Staging layer**: cleans raw trade and user data
- **Mart layer**: defines business-facing tables

Core tables include:
- `fact_trades`: trade-level metrics including volume and revenue
- `dim_users`: user attributes including acquisition channel
- `fct_user_daily_metrics`: aggregated user activity for DAU and retention

This structure enables scalable and consistent metric computation.

---

## KPIs & Metrics

| Metric | Description |
|---|---|
| Daily Active Traders | Unique users trading each day |
| Monthly Volume by Ticker | Total trade value per instrument per month |
| Buy vs Sell Volume | Buy/sell breakdown per ticker |
| User Retention Rate | Monthly retention per user by account type |
| Top Users by Volume | Highest value traders ranked |
| Volume by Country | Geographic breakdown of trading activity |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data Generation | Python, Faker, pandas |
| Storage | DuckDB |
| Transformation | dbt (dbt-duckdb) |
| Testing & Docs | dbt tests, dbt docs |
| Visualization | Streamlit, Plotly |
| Version Control | Git, GitHub |

---

## Project Structure

```
brokerage-kpi/
├── generation/
│   └── generate_data.py        # Generates synthetic users, trades, instruments
├── brokerage_dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_users.sql
│   │   │   ├── stg_trades.sql
│   │   │   ├── stg_instruments.sql
│   │   │   └── schema.yml
│   │   ├── intermediate/
│   │   │   ├── int_user_trade_summary.sql
│   │   │   └── int_monthly_retention.sql
│   │   └── marts/
│   │       ├── fct_daily_active_traders.sql
│   │       ├── fct_volume_by_ticker.sql
│   │       ├── fct_user_metrics.sql
│   │       └── schema.yml
│   └── dbt_project.yml
├── dashboard/
│   └── app.py                  # Streamlit dashboard
├── data/
│   └── exports/                # CSV exports for deployment
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.12

### 1. Clone the repo
```bash
git clone https://github.com/YannnnnaY/brokerage-kpi.git
cd brokerage-kpi
```

### 2. Set up environment
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install duckdb pandas dbt-duckdb streamlit plotly faker
```

### 3. Generate data
```bash
python3 generation/generate_data.py
```

### 4. Run dbt models
```bash
cd brokerage_dbt
dbt run
dbt test
```

### 5. Launch dashboard
```bash
cd ..
streamlit run dashboard/app.py
```

---

## Data Quality Tests

20 dbt tests across all model layers covering:
- `not_null` on all critical columns
- `unique` on primary keys (user_id, trade_id, ticker)
- `accepted_values` on trade_type and account_type

```bash
cd brokerage_dbt
dbt test
```

---

## dbt Documentation

```bash
cd brokerage_dbt
dbt docs generate
dbt docs serve --port 8082
```

---

## Future Improvements
- Replace synthetic data with real market data via broker APIs
- Add Airflow orchestration for daily data refresh
- Migrate to BigQuery for cloud scale
- Add cohort analysis and LTV metrics
- Deploy on Astronomer Cloud
