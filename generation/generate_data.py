import duckdb
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

DB_PATH = "/Users/bliu/LearningProjects/brokerage-kpi/brokerage.duckdb"
TICKERS = ["AAPL", "GOOGL", "JPM", "SPY", "TSLA", "NVDA", "QQQ"]
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 1, 1)

def generate_users(n=1000):
    users = []
    for i in range(1, n + 1):
        signup_date = START_DATE + timedelta(days=random.randint(0, 365))
        users.append({
            "user_id": f"U{i:04d}",
            "name": fake.name(),
            "email": fake.email(),
            "signup_date": signup_date.date(),
            "country": random.choice(["US", "CA", "UK", "AU"]),
            "account_type": random.choice(["basic", "premium", "gold"])
        })
    return pd.DataFrame(users)

def generate_instruments():
    instruments = []
    prices = {
        "AAPL": 185, "GOOGL": 140, "JPM": 195,
        "SPY": 470, "TSLA": 250, "NVDA": 495, "QQQ": 410
    }
    for ticker in TICKERS:
        instruments.append({
            "ticker": ticker,
            "name": ticker,
            "sector": random.choice(["Technology", "Finance", "ETF"]),
            "base_price": prices[ticker]
        })
    return pd.DataFrame(instruments)

def generate_trades(users_df, n=50000):
    trades = []
    user_ids = users_df["user_id"].tolist()

    for i in range(1, n + 1):
        trade_date = START_DATE + timedelta(days=random.randint(0, 730))
        ticker = random.choice(TICKERS)
        base_prices = {
            "AAPL": 185, "GOOGL": 140, "JPM": 195,
            "SPY": 470, "TSLA": 250, "NVDA": 495, "QQQ": 410
        }
        price = round(base_prices[ticker] * random.uniform(0.8, 1.3), 2)
        quantity = random.randint(1, 50)

        trades.append({
            "trade_id": f"T{i:06d}",
            "user_id": random.choice(user_ids),
            "ticker": ticker,
            "trade_date": trade_date.date(),
            "trade_type": random.choice(["buy", "sell"]),
            "quantity": quantity,
            "price": price,
            "total_value": round(price * quantity, 2)
        })
    return pd.DataFrame(trades)

def load_to_duckdb(users_df, instruments_df, trades_df):
    conn = duckdb.connect(DB_PATH)

    conn.execute("DROP TABLE IF EXISTS raw_users")
    conn.execute("DROP TABLE IF EXISTS raw_instruments")
    conn.execute("DROP TABLE IF EXISTS raw_trades")

    conn.execute("""
        CREATE TABLE raw_users AS SELECT * FROM users_df
    """)
    conn.execute("""
        CREATE TABLE raw_instruments AS SELECT * FROM instruments_df
    """)
    conn.execute("""
        CREATE TABLE raw_trades AS SELECT * FROM trades_df
    """)

    print(f"Users: {len(users_df)} rows")
    print(f"Instruments: {len(instruments_df)} rows")
    print(f"Trades: {len(trades_df)} rows")
    conn.close()

if __name__ == "__main__":
    print("Generating data...")
    users_df = generate_users(1000)
    instruments_df = generate_instruments()
    trades_df = generate_trades(users_df, 50000)
    load_to_duckdb(users_df, instruments_df, trades_df)
    print("All done!")
