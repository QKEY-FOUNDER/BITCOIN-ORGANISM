import pandas as pd
import glob
import os

# pasta com os CSVs mensais já fundidos
MONTHLY_DIR = "../../data/07_global_reckoning_2022_infinity"
OUT_PATH = "../../data/normalized/btc_ohlcv_daily.csv"

files = sorted(glob.glob(os.path.join(MONTHLY_DIR, "bitcoin_*.csv")))

if not files:
    raise RuntimeError("Nenhum CSV mensal encontrado")

dfs = []

for f in files:
    df = pd.read_csv(f, parse_dates=["Date"])
    dfs.append(df)

daily = pd.concat(dfs, ignore_index=True)
daily = daily.sort_values("Date")

daily.to_csv(OUT_PATH, index=False)

print("✓ OHLCV diário canónico criado")
print(f"→ {OUT_PATH}")
print(f"Registos: {len(daily)}")

