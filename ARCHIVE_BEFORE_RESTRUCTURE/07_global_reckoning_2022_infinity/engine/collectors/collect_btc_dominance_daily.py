import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

print("🫀 BATIMENTO — Dominance BTC diária (canónico)")

# =========================================================
# PROJECT ROOT (único e absoluto)
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =========================================================
# OUTPUT
# =========================================================
OUT_DIR = PROJECT_ROOT / "data" / "normalized"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = OUT_DIR / "dominance_daily.csv"

# =========================================================
# FETCH DATA (CoinGecko)
# =========================================================
url = "https://api.coingecko.com/api/v3/global"
resp = requests.get(url, timeout=30)

if resp.status_code != 200:
    raise RuntimeError("❌ Falha ao obter dados do CoinGecko")

data = resp.json()["data"]

dominance = data["market_cap_percentage"]["btc"]

today = datetime.now(timezone.utc).date()

row = {
    "Date": today.isoformat(),
    "DominanceBTC": round(float(dominance), 4)
}

# =========================================================
# APPEND (ou criar)
# =========================================================
if OUT_FILE.exists():
    df = pd.read_csv(OUT_FILE)
    if today.isoformat() in df["Date"].values:
        print("⚠️ Dominance de hoje já existe — ignorado")
        exit(0)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
else:
    df = pd.DataFrame([row])

df = df.sort_values("Date")
df.to_csv(OUT_FILE, index=False)

print("✅ Dominance diária registada com sucesso")
print(f"📅 Date: {row['Date']}")
print(f"📊 DominanceBTC: {row['DominanceBTC']}")
print(f"📁 Ficheiro: {OUT_FILE}")
