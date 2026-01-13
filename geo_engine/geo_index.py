import csv
from datetime import datetime
from region_map import REGIONS

def hour_from_timestamp(ts):
    if isinstance(ts, str):
        # tenta ISO, senão assume YYYY-MM-DD
        try:
            dt = datetime.fromisoformat(ts)
        except:
            dt = datetime.strptime(ts, "%Y-%m-%d")
    else:
        dt = datetime.utcfromtimestamp(ts)
    return dt.hour

def hour_overlap(hour, region_hours):
    start, end = region_hours

    if start <= end:
        return 1.0 if start <= hour < end else 0.0
    else:
        # janela que cruza a meia-noite
        return 1.0 if hour >= start or hour < end else 0.0

def compute_geo_dominance(csv_path):
    scores = {r: 0.0 for r in REGIONS}

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row["Date"]
            volume = float(row["Volume"])

            hour = hour_from_timestamp(ts)

            for region, meta in REGIONS.items():
                overlap = hour_overlap(hour, meta["hours"])
                scores[region] += volume * overlap

    total = sum(scores.values())
    if total == 0:
        return scores

    return {r: scores[r] / total for r in scores}

from datetime import datetime

BINANCE_KLINES = "https://api.binance.com/api/v3/klines"

REGION_HOURS = {
    "east_asia": range(0, 9),
    "europe": range(7, 16),
    "north_america": range(13, 22),
    "crypto_native": range(0, 24)
}

def fetch_intraday_volume():
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 24
    }
    data = requests.get(BINANCE_KLINES, params=params).json()
    return data

def compute_intraday_geo_vector():
    candles = fetch_intraday_volume()

    hour_regions = {}

    for c in candles:
        ts = int(c[0]) / 1000
        hour = datetime.utcfromtimestamp(ts).hour
        volume = float(c[5])

        region_weights = {}

        for region, hours in REGION_HOURS.items():
            if hour in hours:
                region_weights[region] = 1.0
            else:
                region_weights[region] = 0.2  # background activity

        # normalize
        total = sum(region_weights.values())
        for r in region_weights:
            region_weights[r] /= total

        # multiply by real traded volume
        for r in region_weights:
            region_weights[r] *= volume

        hour_regions[hour] = region_weights

    return hour_regions
