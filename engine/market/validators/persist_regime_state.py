from pathlib import Path
import pandas as pd
from datetime import datetime, timezone

print("🧠 REGIME STATE — Persistência Evolutiva (EWMA)")

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data" / "market"

DATA_FUSED = DATA_DIR / "final" / "btc_daily_full.csv"
STATE_FILE = DATA_DIR / "output" / "regime_state.csv"
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

# =========================================================
# LOAD DATA
# =========================================================
if not DATA_FUSED.exists():
    raise RuntimeError(f"❌ Dataset fused inexistente: {DATA_FUSED}")

df = pd.read_csv(DATA_FUSED)

if df.empty:
    raise RuntimeError("❌ Dataset vazio")

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# =========================================================
# STRESS SCORE
# =========================================================
df["pct_change"] = df["Close"].pct_change(fill_method=None) * 100
df["volatility"] = df["pct_change"].rolling(5).std()

latest = df.iloc[-1]
stress_score = 0

if abs(latest["pct_change"]) > 5:
    stress_score += 2

if latest["volatility"] > df["volatility"].mean():
    stress_score += 1

if "DominanceBTC" in df.columns:
    dom_std = df["DominanceBTC"].rolling(5).std().iloc[-1]
    if dom_std > df["DominanceBTC"].std():
        stress_score += 1

# =========================================================
# LOAD HISTÓRICO
# =========================================================
if STATE_FILE.exists():
    prev_df = pd.read_csv(STATE_FILE)
else:
    prev_df = pd.DataFrame()

historical_scores = prev_df["stress_score"].tolist() if not prev_df.empty else []
historical_scores.append(stress_score)

temp_df = pd.DataFrame({"stress_score": historical_scores})
temp_df["stress_ewma"] = (
    temp_df["stress_score"]
    .ewm(span=7, adjust=False)
    .mean()
)

stress_ewma = round(temp_df["stress_ewma"].iloc[-1], 4)

# =========================================================
# DERIVADAS
# =========================================================
if not prev_df.empty and "stress_ewma" in prev_df.columns:

    prev_ewma = prev_df["stress_ewma"].iloc[-1]
    stress_velocity = stress_ewma - prev_ewma

    if "stress_velocity" in prev_df.columns and len(prev_df) > 1:
        prev_velocity = prev_df["stress_velocity"].iloc[-1]
        stress_acceleration = stress_velocity - prev_velocity
    else:
        stress_acceleration = 0.0

else:
    stress_velocity = 0.0
    stress_acceleration = 0.0

# =========================================================
# CLASSIFICAÇÃO REGIME
# =========================================================
if stress_ewma >= 3:
    regime = "structural_shift"
elif stress_ewma >= 1.5:
    regime = "volatile"
else:
    regime = "calm"

# =========================================================
# DATA BASEADA NO ÚLTIMO REGISTO DE MERCADO
# =========================================================
last_market_date = df["Date"].iloc[-1].date().isoformat()
today = last_market_date

row = {
    "Date": today,
    "stress_score": stress_score,
    "stress_ewma": stress_ewma,
    "stress_velocity": stress_velocity,
    "stress_acceleration": stress_acceleration,
    "regime": regime,
}

# =========================================================
# APPEND
# =========================================================
if STATE_FILE.exists():
    state_df = pd.read_csv(STATE_FILE)

    if today in state_df["Date"].values:
        print("⚠️ Estado de hoje já registado — ignorado")
        raise SystemExit(0)

    state_df = pd.concat([state_df, pd.DataFrame([row])], ignore_index=True)
else:
    state_df = pd.DataFrame([row])

state_df = state_df.sort_values("Date")
state_df.to_csv(STATE_FILE, index=False)

print("✅ Regime persistido")
print(f"📅 Date: {today}")
print(f"🧮 Stress Score: {stress_score}")
print(f"📉 Stress EWMA: {stress_ewma}")
print(f"🧬 Regime: {regime}")
print(f"📁 Ficheiro: {STATE_FILE}")
