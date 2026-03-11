import requests
import pandas as pd
from datetime import datetime

BTC_API = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
DATA_FILE = "data/btc_price_live.csv"

def fetch_btc_data():

    params = {
        "vs_currency": "usd",
        "days": "365"
    }

    headers = {
        "User-Agent": "bitcoin-organism-observatory"
    }

    r = requests.get(BTC_API, params=params, headers=headers)

    if r.status_code != 200:
        print("API request failed:", r.status_code)
        print(r.text)
        return

    data = r.json()

    if "prices" not in data:
        print("Unexpected API response:", data)
        return

    prices = data["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

    df = df[["date", "price"]]

    df.to_csv(DATA_FILE, index=False)

    print("BTC data updated:", datetime.now())

if __name__ == "__main__":
    fetch_btc_data()
