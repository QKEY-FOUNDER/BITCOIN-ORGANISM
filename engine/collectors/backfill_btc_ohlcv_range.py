import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

print("🔁 BACKFILL — BTC OHLCV RANGE")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "ohlcv"
RAW_DIR.mkdir(parents=True, exist_ok=True)

BINANCE_URL = "https://api.binance.com/api/v3/klines"

def fetch_day(date_str):
    dt = datetime.fromisoformat(date_str)
    start_ts = int(datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc).timestamp() * 1000)
    end_ts = start_ts + 86400000

    params = {
        "symbol": "BTCUSDT",
        "interval": "1d",
        "startTime": start_ts,
        "endTime": end_ts,
        "limit": 1,
    }

    r = requests.get(BINANCE_URL, params=params, timeout=20)

    if r.status_code != 200:
        print(f"❌ Falha Binance para {date_str}")
        return

    data = r.json()
    if not data:
        print(f"⚠️ Sem dados para {date_str}")
        return

    candle = data[0]

    row = {
        "Date": date_str,
        "Open": float(candle[1]),
        "High": float(candle[2]),
        "Low": float(candle[3]),
        "Close": float(candle[4]),
        "Volume": float(candle[5]),
    }

    filename = RAW_DIR / f"btc_ohlcv_{date_str}.csv"

    pd.DataFrame([row]).to_csv(filename, index=False)
    print(f"✅ Backfill criado: {filename}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ Fornece datas: YYYY-MM-DD YYYY-MM-DD ...")
        exit(1)

    for d in sys.argv[1:]:
        fetch_day(d)
