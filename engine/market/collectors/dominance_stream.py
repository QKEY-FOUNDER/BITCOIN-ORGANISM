from pathlib import Path
import requests
from datetime import datetime, timedelta, timezone
import csv
import time

# =========================================================
# DOMINANCE STREAM — BTC DAILY (INFINITO)
# Pilar macro do organismo
# =========================================================

COINGECKO_URL = "https://api.coingecko.com/api/v3/global"

ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data" / "dominance"

START_DATE = datetime(2026, 1, 1, tzinfo=timezone.utc)

print("🩸 DOMINANCE STREAM — BTC DAILY")
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


def fetch_dominance():
    r = requests.get(COINGECKO_URL)
    r.raise_for_status()
    data = r.json()
    return data["data"]["market_cap_percentage"]["btc"]


def write_day(day, dominance):
    year = f"{day.year}"
    month = f"{day.year}_{day.month:02d}"
    path = DATA_ROOT / year / month
    path.mkdir(parents=True, exist_ok=True)

    file = path / f"{day.strftime('%Y_%m_%d')}.csv"

    if file.exists():
        return False

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "dominance_btc"])
        writer.writerow([
            day.strftime("%Y-%m-%d"),
            round(float(dominance), 4)
        ])

    return True


# ---------------------------------------------------------
# EXECUÇÃO
# ---------------------------------------------------------

today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

last = last_saved_date()
current = (last + timedelta(days=1)) if last else START_DATE

if current > today:
    print("ℹ️ Dominance atualizado — nenhum dia em falta")
    exit(0)

while current <= today:
    print(f"📅 Processando {current.date()}")

    try:
        dominance = fetch_dominance()
        written = write_day(current, dominance)

        if written:
            print("  ✔ gravado")
        else:
            print("  ↪ já existia")

    except Exception as e:
        print("  ❌ erro:", e)

    current += timedelta(days=1)
    time.sleep(1.2)  # respeito biológico à API

print("✅ DOMINANCE STREAM concluído")
