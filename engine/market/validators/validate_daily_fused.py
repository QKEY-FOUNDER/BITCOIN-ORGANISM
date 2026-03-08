from pathlib import Path
import pandas as pd
import subprocess

# =========================================================
# VALIDAÇÃO — BTC DAILY FUSED
# STREAM VIVO + INTEGRIDADE TEMPORAL (RESILIENTE)
# =========================================================

print("VALIDACAO — BTC DAILY FUSED (STREAM VIVO)")
print("=" * 50)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data" / "market"
DATA_FUSED = DATA_DIR / "final" / "btc_daily_full.csv"

if not DATA_FUSED.exists():
    print(f"Ficheiro fused nao encontrado: {DATA_FUSED}")
    exit(1)

df = pd.read_csv(DATA_FUSED)

if df.empty:
    print("Ficheiro fused vazio")
    exit(1)

required_columns = {"Date", "Open", "High", "Low", "Close"}
missing_cols = required_columns - set(df.columns)

if missing_cols:
    print(f"Colunas em falta: {missing_cols}")
    exit(1)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.sort_values("Date").reset_index(drop=True)

expected_range = pd.date_range(
    start=df["Date"].min(),
    end=df["Date"].max(),
    freq="D"
)

actual_dates = df["Date"].dropna()
missing_dates = expected_range.difference(actual_dates)

last_date = df["Date"].max()
df_confirmed = df[df["Date"] < last_date]

if "DominanceBTC" in df.columns:
    missing_dom = df_confirmed["DominanceBTC"].isna().sum()
else:
    missing_dom = len(df_confirmed)

total_confirmed = len(df_confirmed)
coverage = 100 if total_confirmed == 0 else 100 * (1 - missing_dom / total_confirmed)

print(f"Dias sem Dominance: {missing_dom}")
print(f"Cobertura Dominance: {coverage:.2f}%")
print(f"Registos totais: {len(df)}")
print(f"Intervalo: {df['Date'].min().date()} -> {df['Date'].max().date()}")

if len(missing_dates) > 0:
    print("Lacunas temporais detectadas:")
    for d in missing_dates[:10]:
        print(d.date())
else:
    print("Sem lacunas temporais")

if len(missing_dates) > 0:
    backfill_script = PROJECT_ROOT / "engine" / "market" / "collectors" / "backfill_btc_ohlcv_range.py"

    if backfill_script.exists():
        for d in missing_dates:
            subprocess.run(
                ["python3", str(backfill_script), str(d.date())],
                check=True
            )
    else:
        print("Backfill OHLCV nao disponivel - ignorado")

dom_script = PROJECT_ROOT / "engine" / "market" / "collectors" / "backfill_btc_dominance_range.py"

if dom_script.exists():
    for gap_date in missing_dates:
        subprocess.run(
            ["python3", str(dom_script), str(gap_date.date()), str(gap_date.date())]
        )
else:
    print("Backfill Dominance nao disponivel - ignorado")

print("Validacao concluida com sucesso")
