from pathlib import Path
import requests
from datetime import datetime, timedelta, timezone
import csv
import time

# =========================================================
# OHLCV STREAM — BTC DAILY (INFINITO)
# Pilar físico do organismo
# =========================================================

SYMBOL = "BTCUSDT"
INTERVAL = "1d"
BINANCE_URL = "https://api.binance.com/api/v3/klines"

ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data" / "ohlcv"

START_DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)

print("🫀 OHLCV STREAM — BTC DAILY")
print("=" * 50)

# ---------------------------------------------------------
# UTILIDADES
# ---------------------------------------------------------

def last_saved_date():
    if not DATA_ROOT.exists():
        return None

    dates = []
    for year_dir in DATA_ROOT.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            for f in month_dir.glob("*.csv"):
                try:
                    d = datetime.strptime(f.stem, "%Y_%m_%d")
                    dates.append(d)
                except:
                    pass

    return max(dates) if dates else None


def fetch_day(day):
    start = int(day.timestamp() * 1000)
    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "startTime": start,
        "limit": 1
    }
    r = requests.get(BINANCE_URL, params=params)
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def write_day(day, candle):
    year = f"{day.year}"
    month = f"{day.year}_{day.month:02d}"
    path = DATA_ROOT / year / month
    path.mkdir(parents=True, exist_ok=True)

    file = path / f"{day.strftime('%Y_%m_%d')}.csv"

    if file.exists():
        return False

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "open", "high", "low", "close", "volume"])
        writer.writerow([
            day.strftime("%Y-%m-%d"),
            candle[1],
            candle[2],
            candle[3],
            candle[4],
            candle[5]
        ])

    return True


# ---------------------------------------------------------
# EXECUÇÃO
# ---------------------------------------------------------

today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

last = last_saved_date()
current = (last + timedelta(days=1)) if last else START_DATE

if current > today:
    print("ℹ️ OHLCV atualizado — nenhum dia em falta")
    exit(0)

while current <= today:
    print(f"📅 Processando {current.date()}")

    candle = fetch_day(current)
    if candle:
        written = write_day(current, candle)
        if written:
            print("  ✔ gravado")
        else:
            print("  ↪ já existia")
    else:
        print("  ⚠️ sem dados")

    current += timedelta(days=1)
    time.sleep(0.3)

print("✅ OHLCV STREAM concluído")
