from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("BTCONIC ANALYSIS v2 - Evolucao Quantitativa")

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data" / "market"

HISTORY_FILE = DATA_DIR / "output" / "btconic_history.csv"
BTC_FILE = DATA_DIR / "final" / "btc_daily_full.csv"

if not HISTORY_FILE.exists() or not BTC_FILE.exists():
    raise RuntimeError("Ficheiros necessarios nao encontrados")

history = pd.read_csv(HISTORY_FILE, parse_dates=["Date"])
btc = pd.read_csv(BTC_FILE, parse_dates=["Date"])

df = pd.merge(history, btc[["Date", "Close"]], on="Date", how="inner")

df = df.sort_values("Date")

# -----------------------------
# Retornos
# -----------------------------
df["return_1d"] = df["Close"].pct_change()
df["return_3d_fwd"] = df["Close"].pct_change(3).shift(-3)
df["return_7d_fwd"] = df["Close"].pct_change(7).shift(-7)

# -----------------------------
# Rolling correlation (janela 10)
# -----------------------------
df["rolling_corr_1d"] = (
    df["risk_score"]
    .rolling(10)
    .corr(df["return_1d"])
)

# -----------------------------
# Clusters de risco elevado
# -----------------------------
risk_threshold = 0.6
df["high_risk"] = df["risk_score"] > risk_threshold

high_risk_periods = df[df["high_risk"]]

# -----------------------------
# Estatistica condicional
# -----------------------------
mean_return_after_high_risk = (
    df[df["high_risk"]]["return_3d_fwd"].mean()
)

print("\n--- Estatisticas ---")
print("Total observacoes:", len(df))
print("Media retorno 3D apos risco alto:", round(mean_return_after_high_risk, 4))

# -----------------------------
# Visualizacao
# -----------------------------
plt.figure(figsize=(12,7))

# Risk score
plt.plot(df["Date"], df["risk_score"], label="Risk Score", linewidth=2)

# BTC normalizado
plt.plot(
    df["Date"],
    df["Close"]/df["Close"].max(),
    label="BTC Normalizado",
    alpha=0.7
)

# Marcar zonas de risco alto
plt.scatter(
    high_risk_periods["Date"],
    high_risk_periods["risk_score"],
    color="red",
    label="High Risk",
    zorder=5
)

plt.title("BTConic Risk Score vs BTC - Evolucao")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
