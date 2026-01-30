from pathlib import Path
import sys
import requests
import pandas as pd
from datetime import datetime

# =========================================================
# BACKFILL — BTC DOMINANCE DAILY
# Uma data → uma chamada → uma escrita (se faltar)
# =========================================================

print("🧬 BACKFILL — BTC DOMINANCE DAILY")
print("=" * 50)

# ---------------------------------------------------------
# ARGUMENTO
# ---------------------------------------------------------

if len(sys.argv) != 2:
    print("Uso: python3 backfill_btc_dominance_daily.py YYYY-MM-DD")
    sys.exit(1)

target_date = sys.argv[1]

try:
    datetime.strptime(target_date, "%Y-%m-%d")
except ValueError:
    print("❌ Data inválida. Usa formato YYYY-MM-DD")
    sys.exit(1)

print(f"📅 Data alvo: {target_date}")

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_PATH = Path(__file__).resolve().parents[2]
DATA_NORM = BASE_PATH / "data/normalized"
DATA_NORM.mkdir(parents=True, exist_ok=True)

DOM_FILE = DATA_NORM / "dominance_daily.csv"

# ---------------------------------------------------------
# LOAD EXISTING
# ---------------------------------------------------------

if DOM_FILE.exists():
    df = pd.read_csv(DOM_FILE)
else:
    df = pd.DataFrame(columns=["Date", "DominanceBTC"])

if target_date in df["Date"].values:
    print("🟡 Dominance já existe para esta data. Nenhuma ação tomada.")
    sys.exit(0)

# ---------------------------------------------------------
# FETCH COINGECKO (1 chamada)
# ---------------------------------------------------------

url = "https://api.coingecko.com/api/v3/global"
print("🌍 A recolher Dominance BTC (1 chamada API)")

try:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    dominance = data["data"]["market_cap_percentage"]["btc"]
except Exception as e:
    print(f"❌ Erro ao obter dados: {e}")
    sys.exit(1)

print(f"📊 DominanceBTC: {dominance}")

# ---------------------------------------------------------
# APPEND + SORT
# ---------------------------------------------------------

df = pd.concat(
    [df, pd.DataFrame([{
        "Date": target_date,
        "DominanceBTC": round(float(dominance), 6)
    }])],
    ignore_index=True
)

df = df.sort_values("Date")
df.to_csv(DOM_FILE, index=False)

# ---------------------------------------------------------
# FINAL
# ---------------------------------------------------------

print("✅ Dominance registada com sucesso")
print(f"📄 Ficheiro: {DOM_FILE}")
print("🧠 Backfill concluído com integridade")
