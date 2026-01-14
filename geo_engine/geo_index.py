import os
import csv
import requests
from datetime import datetime
from geo_engine.region_map import REGIONS

BINANCE_KLINES = "https://api.binance.com/api/v3/klines"

# Pasta onde a memória geográfica histórica vive
DATA_GEO_PATH = "data_geo/monthly_region_dominance"


# -----------------------------
# Time utilities
# -----------------------------

def extract_month_from_csv(csv_path):
    # Ex: data/.../bitcoin_2017_12.csv → 2017_12
    name = os.path.basename(csv_path)
    parts = name.replace(".csv", "").split("_")
    return parts[1] + "_" + parts[2]


# -----------------------------
# Historical memory
# -----------------------------

def load_historical_geo(month):
    path = os.path.join(DATA_GEO_PATH, f"{month}.csv")

    if not os.path.exists(path):
        return None

    geo = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            geo[r["region"]] = float(r["dominance"])

    return geo


# -----------------------------
# Live Binance perception
# -----------------------------

def fetch_intraday_volume():
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 24
    }
    return requests.get(BINANCE_KLINES, params=params).json()


def compute_live_geo():
    candles = fetch_intraday_volume()

    scores = {r: 0.0 for r in REGIONS}

    for c in candles:
        ts = int(c[0]) / 1000
        volume = float(c[5])
        hour = datetime.utcfromtimestamp(ts).hour

        for region, meta in REGIONS.items():
            start, end = meta["hours"]

            # janela normal
            if start <= end:
                active = start <= hour < end
            else:
                # cruza a meia-noite
                active = hour >= start or hour < end

            weight = 1.0 if active else 0.2
            scores[region] += volume * weight

    total = sum(scores.values())
    if total == 0:
        return scores

    return {r: scores[r] / total for r in scores}


# -----------------------------
# Unified geographic brain
# -----------------------------

def get_geo_vector(csv_path):
    month = extract_month_from_csv(csv_path)

    # 1. Tenta memória histórica
    historical = load_historical_geo(month)
    if historical:
        return historical

    # 2. Caso contrário, vê o mundo em tempo real
    return compute_live_geo()
