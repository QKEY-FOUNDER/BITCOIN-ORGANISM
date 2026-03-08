from pathlib import Path
import pandas as pd
import numpy as np

print("🧠 MONITOR — Anomalias Estatísticas BTC")
print("=" * 50)

# =========================================================
# PATHS
# =========================================================
BASE_PATH = Path(__file__).resolve().parents[2]
DATA_FUSED = BASE_PATH / "data/final/btc_daily_full.csv"

if not DATA_FUSED.exists():
    print("❌ Dataset fused não encontrado")
    exit(1)

df = pd.read_csv(DATA_FUSED)

if len(df) < 10:
    print("⚠️ Histórico insuficiente para análise estatística robusta")
    exit(0)

# =========================================================
# PREPARAÇÃO
# =========================================================
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df = df.dropna(subset=["Close"]).copy()

df["return_pct"] = df["Close"].pct_change(fill_method=None) * 100

# =========================================================
# 1️⃣ Z-SCORE DE RETORNOS
# =========================================================
mean_ret = df["return_pct"].mean()
std_ret  = df["return_pct"].std()

df["z_score"] = (df["return_pct"] - mean_ret) / std_ret

extreme_moves = df[np.abs(df["z_score"]) > 3]

# =========================================================
# 2️⃣ VOLATILIDADE ROLLING
# =========================================================
df["rolling_vol"] = df["return_pct"].rolling(7).std()

vol_threshold = df["rolling_vol"].mean() + 2 * df["rolling_vol"].std()
vol_spikes = df[df["rolling_vol"] > vol_threshold]

# =========================================================
# 3️⃣ DOMINANCE SHOCK
# =========================================================
dominance_spikes = pd.DataFrame()

if "DominanceBTC" in df.columns:
    df["dom_change"] = df["DominanceBTC"].pct_change(fill_method=None) * 100
    dom_std = df["dom_change"].std()
    dominance_spikes = df[np.abs(df["dom_change"]) > 2 * dom_std]

# =========================================================
# 4️⃣ SCORE DE STRESS
# =========================================================
stress_score = (
    len(extreme_moves) * 2 +
    len(vol_spikes) * 2 +
    len(dominance_spikes) * 1
)

# =========================================================
# RELATÓRIO
# =========================================================
print(f"📊 Total de registos analisados: {len(df)}")

if extreme_moves.empty:
    print("✅ Sem movimentos extremos relevantes")
else:
    print(f"⚠️ Movimentos extremos detectados: {len(extreme_moves)}")

if vol_spikes.empty:
    print("✅ Volatilidade dentro do regime esperado")
else:
    print(f"⚠️ Picos de volatilidade detectados: {len(vol_spikes)}")

if dominance_spikes.empty:
    print("✅ Dominance estável")
else:
    print(f"⚠️ Alterações abruptas de dominance: {len(dominance_spikes)}")

print(f"🧮 Stress Score: {stress_score}")

if stress_score == 0:
    print("🟢 Estado estatístico saudável")
elif stress_score < 5:
    print("🟡 Mercado em regime de alerta moderado")
else:
    print("🔴 Mercado em regime de stress elevado")

print("\n🧠 Monitor estatístico evolutivo concluído.")
