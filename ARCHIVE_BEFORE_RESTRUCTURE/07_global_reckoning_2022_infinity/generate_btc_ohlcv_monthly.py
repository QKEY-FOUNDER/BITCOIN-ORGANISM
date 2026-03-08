import requests
import pandas as pd
from datetime import datetime, timedelta
import time

BASE_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"

START_DATE = "2024-10-01"
END_DATE   = "2025-12-31"

def daterange_months(start, end):
    current = start.replace(day=1)
    while current <= end:
        yield current
        if current.month == 12:
            current = current.replace(year=current.year+1, month=1)
        else:
            current = current.replace(month=current.month+1)

def fetch_ohlcv(start_date, end_date):
    params = {
        "vs_currency": "usd",
        "from": int(start_date.timestamp()),
        "to": int(end_date.timestamp())
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json()

    prices = data["prices"]
    volumes = dict(data["total_volumes"])

    rows = []
    for ts, price in prices:
        date = datetime.utcfromtimestamp(ts/1000).date()
        rows.append({
            "Date": date,
            "Price": price,
            "Volume": volumes.get(ts, None)
        })

    df = pd.DataFrame(rows)
    df = df.groupby("Date").agg(
        Open=("Price","first"),
        High=("Price","max"),
        Low=("Price","min"),
        Close=("Price","last"),
        Volume=("Volume","sum")
    ).reset_index()

    return df

start = datetime.strptime(START_DATE, "%Y-%m-%d")
end   = datetime.strptime(END_DATE, "%Y-%m-%d")

for month_start in daterange_months(start, end):
    if month_start.month == 12:
        month_end = month_start.replace(day=31)
    else:
        month_end = (month_start.replace(month=month_start.month+1, day=1) - timedelta(days=1))

    print(f"📥 Fetching {month_start:%Y-%m}")
    df = fetch_ohlcv(month_start, month_end)

    fname = f"bitcoin_{month_start:%Y_%m}.csv"
    df.to_csv(fname, index=False)
    print(f"✅ Criado {fname}")

    time.sleep(12)
