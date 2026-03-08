import pandas as pd
from pathlib import Path

# --------------------------------------------------
# BASE DIR (BITCOIN-ORGANISM/data)
# collectors → engine → 07_global_reckoning_2022_infinity → data
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "data"
NORMALIZED_DIR = DATA_DIR / "normalized"
FINAL_DIR = DATA_DIR / "final"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

OHLCV_FILE = NORMALIZED_DIR / "btc_ohlcv_daily.csv"
DOM_FILE = NORMALIZED_DIR / "dominance_daily.csv"
OUT_FILE = FINAL_DIR / "btc_daily_FULL.csv"

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------
if not OHLCV_FILE.exists():
    raise RuntimeError(f"❌ OHLCV diário não encontrado: {OHLCV_FILE}")

if not DOM_FILE.exists():
    raise RuntimeError(f"❌ Dominância diária não encontrada: {DOM_FILE}")

# --------------------------------------------------
# LOAD
# --------------------------------------------------
ohlcv = pd.read_csv(OHLCV_FILE, parse_dates=["Date"])
dom = pd.read_csv(DOM_FILE, parse_dates=["Date"])

# --------------------------------------------------
# MERGE
# --------------------------------------------------
df = pd.merge(
    ohlcv,
    dom[["Date", "BTC_Dominance"]],
    on="Date",
    how="left"
)

df = df.sort_values("Date")
df.to_csv(OUT_FILE, index=False)

# --------------------------------------------------
# REPORT
# --------------------------------------------------
print("🧬 MERGE DIÁRIO CONCLUÍDO")
print(f"📁 Ficheiro: {OUT_FILE}")
print(f"📊 Registos: {len(df)}")
print(f"🕰 Intervalo: {df['Date'].min().date()} → {df['Date'].max().date()}")
