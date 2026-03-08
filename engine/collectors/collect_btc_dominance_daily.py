import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

print("🫀 BATIMENTO — Dominance BTC diária (RAW)")

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =========================================================
# RAW OUTPUT DIRECTORY
# =========================================================
RAW_DIR = PROJECT_ROOT / "engine" / "collectors" / "data" / "raw" / "dominance"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Ficheiro mensal (crescimento orgânico acumulativo)
today = datetime.now(timezone.utc).date()
year_month = today.strftime("%Y_%m")
OUT_FILE = RAW_DIR / f"btc_dominance_{year_month}_raw.csv"

# =========================================================
# FETCH DATA (CoinGecko)
# =========================================================
url = "https://api.coingecko.com/api/v3/global"
resp = requests.get(url, timeout=30)

if resp.status_code != 200:
    raise RuntimeError("❌ Falha ao obter dados do CoinGecko")

data = resp.json().get("data", {})
dominance = data.get("market_cap_percentage", {}).get("btc")

if dominance is None:
    raise RuntimeError("❌ Dominance BTC não encontrada na resposta")

row = {
    "Date": today.isoformat(),
    "DominanceBTC": round(float(dominance), 4)
}

# =========================================================
# APPEND OR CREATE (RAW)
# =========================================================
if OUT_FILE.exists():
    df = pd.read_csv(OUT_FILE)

    if today.isoformat() in df["Date"].values:
        print("⚠️ Dominance de hoje já existe no RAW — ignorado")
        exit(0)

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
else:
    df = pd.DataFrame([row])

df = df.sort_values("Date")
df.to_csv(OUT_FILE, index=False)

print("✅ Dominance RAW registada com sucesso")
print(f"📅 Date: {row['Date']}")
print(f"📊 DominanceBTC: {row['DominanceBTC']}")
print(f"📁 Ficheiro RAW: {OUT_FILE}")
