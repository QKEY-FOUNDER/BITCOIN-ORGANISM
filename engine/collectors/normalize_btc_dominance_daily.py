from pathlib import Path
import pandas as pd

print("📊 NORMALIZAÇÃO BTC DOMINANCE — HÍBRIDO PROFISSIONAL")
print("=" * 55)

# =========================================================
# ROOT
# =========================================================

BASE_PATH = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_PATH / "data/raw/dominance"
OUT_PATH = BASE_PATH / "data/normalized/dominance_daily.csv"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# 1️⃣ HISTÓRICO MANUAL (PRIORIDADE MÁXIMA)
# =========================================================

historical_file = RAW_DIR / "btc_dominance_historical.csv"

if historical_file.exists():
    df_hist = pd.read_csv(historical_file)

    if not {"Date", "DominanceBTC"}.issubset(df_hist.columns):
        raise RuntimeError("❌ Histórico manual inválido")

    df_hist["Date"] = pd.to_datetime(df_hist["Date"])
    df_hist["source"] = "historical"

    print(f"✔ Histórico manual carregado: {len(df_hist)} registos")
else:
    df_hist = pd.DataFrame(columns=["Date", "DominanceBTC", "source"])
    print("ℹ Sem histórico manual")

# =========================================================
# 2️⃣ STREAM DIÁRIO
# =========================================================

stream_files = sorted(RAW_DIR.glob("btc_dominance_*.csv"))

stream_rows = []

for f in stream_files:
    if f.name == "btc_dominance_historical.csv":
        continue

    df = pd.read_csv(f)

    if df.empty:
        continue

    if not {"Date", "DominanceBTC"}.issubset(df.columns):
        print(f"⚠ Ignorado (colunas inválidas): {f.name}")
        continue

    df["Date"] = pd.to_datetime(df["Date"])
    df["source"] = "stream"

    stream_rows.append(df)

if stream_rows:
    df_stream = pd.concat(stream_rows, ignore_index=True)
    print(f"✔ Stream diário carregado: {len(df_stream)} registos")
else:
    df_stream = pd.DataFrame(columns=["Date", "DominanceBTC", "source"])
    print("ℹ Sem stream diário")

# =========================================================
# 3️⃣ CONSOLIDAÇÃO
# =========================================================

combined = pd.concat([df_stream, df_hist], ignore_index=True)

if combined.empty:
    raise RuntimeError("❌ Nenhum dado dominance encontrado")

# Prioridade: histórico manual
combined = combined.sort_values(
    by=["Date", "source"],
    ascending=[True, False]  # historical > stream
)

combined = combined.drop_duplicates(subset=["Date"], keep="first")

combined = combined.sort_values("Date")

# Remover coluna técnica
final_df = combined[["Date", "DominanceBTC"]]

# =========================================================
# 4️⃣ EXPORT
# =========================================================

final_df.to_csv(OUT_PATH, index=False)

print("✅ Dominance consolidado com sucesso")
print(f"📁 Ficheiro: {OUT_PATH}")
print(f"📊 Registos finais: {len(final_df)}")
print(f"📆 Intervalo: {final_df['Date'].min().date()} → {final_df['Date'].max().date()}")
