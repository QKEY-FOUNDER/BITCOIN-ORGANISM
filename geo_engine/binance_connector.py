import requests
import time
from datetime import datetime

BINANCE_BASE_URL = "https://api.binance.com"
KLINES_ENDPOINT = "/api/v3/klines"

def get_klines(symbol="BTCUSDT", interval="1m", start_ts=None, end_ts=None, limit=1000):
    """
    Fetch klines (candles) from Binance.

    Returns a list of candles:
    [
        [
            open_time,
            open,
            high,
            low,
            close,
            volume,
            close_time,
            quote_asset_volume,
            number_of_trades,
            taker_buy_base_volume,
            taker_buy_quote_volume,
            ignore
        ],
        ...
    ]
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    if start_ts:
        params["startTime"] = start_ts
    if end_ts:
        params["endTime"] = end_ts

    response = requests.get(BINANCE_BASE_URL + KLINES_ENDPOINT, params=params)
    response.raise_for_status()
    return response.json()


def fetch_month(symbol, year, month):
    """
    Download all 1-minute candles for a given month.
    Returns a list of klines.
    """

    start = int(datetime(year, month, 1).timestamp() * 1000)

    if month == 12:
        end = int(datetime(year + 1, 1, 1).timestamp() * 1000)
    else:
        end = int(datetime(year, month + 1, 1).timestamp() * 1000)

    all_data = []
    current = start

    while current < end:
        print("Fetching from", datetime.utcfromtimestamp(current / 1000))

        batch = get_klines(
            symbol=symbol,
            interval="1m",
            start_ts=current,
            end_ts=end,
            limit=1000
        )

        if not batch:
            break

        all_data.extend(batch)
        current = batch[-1][0] + 1  # move forward
        time.sleep(0.3)  # avoid rate limits

    return all_data


if __name__ == "__main__":
    # Test download: September 2024
    data = fetch_month("BTCUSDT", 2024, 9)
    print("Candles downloaded:", len(data))
