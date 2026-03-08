import requests
import csv
from pathlib import Path
from datetime import datetime

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

OUTPUT_FILE = DATA_PATH / "btc_monthly_ohlcv.csv"

API_URL = "https://api.binance.com/api/v3/klines"

SYMBOL = "BTCUSDT"
INTERVAL = "1M"


def fetch_data():

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": 1000
    }

    response = requests.get(API_URL, params=params)

    data = response.json()

    return data


def save_csv(data):

    with open(OUTPUT_FILE, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "timestamp",
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ])

        for row in data:

            ts = row[0] / 1000
            date = datetime.utcfromtimestamp(ts).strftime("%Y-%m")

            writer.writerow([
                row[0],
                date,
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ])


def main():

    print("\nBitcoin Organism — Market Data Sensor")
    print("--------------------------------------------------")

    data = fetch_data()

    save_csv(data)

    print("Market data updated:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
