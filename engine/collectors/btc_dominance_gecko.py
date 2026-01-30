import requests
import csv
import os
from datetime import datetime, timezone

# -------------------------
# CONFIG
# -------------------------
COINGECKO_URL = "https://api.coingecko.com/api/v3/global"
RAW_DIR = "data/raw/dominance"

# -------------------------
# TIME (UTC DAY)
# -------------------------
now_utc = datetime.now(timezone.utc)
date_str = now_utc.strftime("%Y-%m-%d")
year_month = now_utc.strftime("%Y_%m")

# -------------------------
# FILE PATH
# -------------------------
os.makedirs(RAW_DIR, exist_ok=True)
file_path = f"{RAW_DIR}/btc_dominance_{year_month}_raw.csv"

# -------------------------
# FETCH DATA
# -------------------------
response = requests.get(COINGECKO_URL, timeout=20)
response.raise_for_status()

data = response.json()
dominance = data["data"]["market_cap_percentage"]["btc"]

# -------------------------
# WRITE (APPEND-ONLY)
# -------------------------
file_exists = os.path.isfile(file_path)

with open(file_path, mode="a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["Date", "DominanceBTC"])

    # prevent duplicate dates
    if file_exists:
        with open(file_path, "r") as r:
            if date_str in r.read():
                print("⚠️ Dominance already recorded for today.")
                exit(0)

    writer.writerow([date_str, round(dominance, 2)])

print(f"✅ BTC Dominance recorded: {date_str} → {dominance:.2f}%")
