import pandas as pd
from pathlib import Path

print("🧠 REGIME → ALOCAÇÃO")

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data" / "market"

REGIME_FILE = DATA_DIR / "output" / "regime_state.csv"
MARKET_FILE = DATA_DIR / "final" / "btc_daily_full.csv"
OUT_FILE    = DATA_DIR / "output" / "allocation_state.csv"

# =========================================================
# VALIDATION
# =========================================================
if not REGIME_FILE.exists():
    raise RuntimeError(f"❌ regime_state.csv não encontrado: {REGIME_FILE}")

if not MARKET_FILE.exists():
    raise RuntimeError(f"❌ btc_daily_full.csv não encontrado: {MARKET_FILE}")

# =========================================================
# LOAD
# =========================================================
regime_df = pd.read_csv(REGIME_FILE)
market_df = pd.read_csv(MARKET_FILE, parse_dates=["Date"])

if regime_df.empty:
    raise RuntimeError("❌ regime_state.csv vazio")

if market_df.empty:
    raise RuntimeError("❌ btc_daily_full.csv vazio")

latest_regime = regime_df.iloc[-1]
latest_price  = market_df.iloc[-1]["Close"]

regime = latest_regime["regime"]

# =========================================================
# ALOCAÇÃO BASEADA EM REGIME
# =========================================================
if regime == "calm":
    btc_weight = 0.8
elif regime == "volatile":
    btc_weight = 0.5
elif regime == "structural_shift":
    btc_weight = 0.2
else:
    btc_weight = 0.0

allocation = pd.DataFrame([{
    "Date": latest_regime["Date"],
    "Regime": regime,
    "BTC_Weight": btc_weight,
    "Cash_Weight": round(1 - btc_weight, 4),
    "BTC_Price": latest_price
}])

# =========================================================
# SAVE
# =========================================================
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
allocation.to_csv(OUT_FILE, index=False)

print("✅ Alocação calculada")
print(allocation)
print(f"📁 Ficheiro: {OUT_FILE}")
