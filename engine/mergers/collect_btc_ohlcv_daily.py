import requests
import pandas as pd
from datetime import datetime, timezone

# CONFIG
SYMBOL = "BTCUSDT"
INTERVAL = "1d"
LIMIT = 2  # último candle fechado
URL = "https://api.binance.com/api/v3/klines"

OUT_DIR = "../../data/raw/ohlcv"

params = {
    "symbol": SYMBOL,
    "interval": INTERVAL,
    "limit": LIMIT
}

r = requests.get(URL, params=params)
r.raise_for_status()
data = r.json()

# usar apenas o último candle FECHADO
candle = data[-2]

columns = [
    "timestamp", "Open", "High", "Low", "Close", "Volume",
    "close_time", "quote_volume", "trades",
    "taker_base", "taker_quote", "ignore"
]

df = pd.DataFrame([candle], columns=columns)

df["Date"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True).dt.strftime("%Y-%m-%d")
df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

date = df.iloc[0]["Date"]
out_path = f"{OUT_DIR}/btc_{date}.csv"

df.to_csv(out_path, index=False)
print(f"🟢 OHLCV diário gravado: {out_path}")
