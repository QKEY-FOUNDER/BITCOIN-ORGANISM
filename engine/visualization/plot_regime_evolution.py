from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

print("📊 PLOT — Regime Evolution")

BASE_PATH = Path(__file__).resolve().parents[2]

FUSED_PATH = BASE_PATH / "data/final/btc_daily_full.csv"
STATE_PATH = BASE_PATH / "data/output/regime_state.csv"
OUT_FILE   = BASE_PATH / "data/output/regime_plot.png"

if not FUSED_PATH.exists() or not STATE_PATH.exists():
    raise RuntimeError("❌ Ficheiros necessários inexistentes")

df_price = pd.read_csv(FUSED_PATH)
df_state = pd.read_csv(STATE_PATH)

df_price["Date"] = pd.to_datetime(df_price["Date"])
df_state["Date"] = pd.to_datetime(df_state["Date"])

df = pd.merge(df_price, df_state, on="Date", how="left")

plt.figure(figsize=(12, 6))

plt.plot(df["Date"], df["Close"], label="BTC Close")
plt.plot(df["Date"], df["stress_ewma"], label="Stress EWMA")

plt.title("BTC Regime Evolution")
plt.legend()
plt.tight_layout()

plt.savefig(OUT_FILE)

print(f"✅ Gráfico criado: {OUT_FILE}")
