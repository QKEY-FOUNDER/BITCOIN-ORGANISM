import pandas as pd
from pathlib import Path

print("🔥 SCRIPT CARREGADO — BATIMENTO 4 🔥")

# =========================================================
# PROJECT ROOT (CORRETO E ÚNICO)
# engine/mergers → engine → 07_global_reckoning_2022_infinity
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =========================================================
# PATHS REAIS NO DISCO
# =========================================================
NORMALIZED_DIR = PROJECT_ROOT / "data" / "normalized"
FINAL_DIR = PROJECT_ROOT / "data" / "final"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

OHLCV_FILE = NORMALIZED_DIR / "btc_ohlcv_daily.csv"
DOM_FILE   = NORMALIZED_DIR / "dominance_daily.csv"
OUT_FILE   = FINAL_DIR / "btc_daily_FULL.csv"

# =========================================================
# GUARDAS ABSOLUTAS
# =========================================================
if not OHLCV_FILE.exists():
    raise RuntimeError(f"❌ OHLCV diário não encontrado: {OHLCV_FILE}")

if not DOM_FILE.exists():
    raise RuntimeError(f"❌ Dominância diária não encontrada: {DOM_FILE}")

# =========================================================
# LOAD DATA
# =========================================================
ohlcv = pd.read_csv(OHLCV_FILE, parse_dates=["Date"])
dom   = pd.read_csv(DOM_FILE, parse_dates=["Date"])

# =========================================================
# MERGE
# =========================================================
merged = (
    pd.merge(ohlcv, dom, on="Date", how="left")
      .sort_values("Date")
)

merged.to_csv(OUT_FILE, index=False)

# =========================================================
# REPORT
# =========================================================
print("🟢 BTC DAILY FULL CRIADO COM SUCESSO")
print(f"📄 Ficheiro: {OUT_FILE}")
print(f"📊 Registos: {len(merged)}")
print(f"📆 Intervalo: {merged['Date'].min().date()} → {merged['Date'].max().date()}")
