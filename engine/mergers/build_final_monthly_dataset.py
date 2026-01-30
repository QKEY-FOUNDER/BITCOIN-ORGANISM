from pathlib import Path
import pandas as pd

# diretório deste script
BASE_DIR = Path(__file__).resolve().parent

# pasta final correta
FINAL_DIR = (BASE_DIR / "../../final").resolve()

print(f"🔎 A procurar CSVs em: {FINAL_DIR}")

csv_files = sorted(FINAL_DIR.glob("bitcoin_*.csv"))
print(f"📄 Encontrados: {len(csv_files)} ficheiros")

if not csv_files:
    raise RuntimeError("Nenhum CSV mensal encontrado")

# juntar tudo num único dataframe
dfs = []
for f in csv_files:
    df = pd.read_csv(f, parse_dates=["Date"])
    dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)
final_df = final_df.sort_values("Date")

out_path = FINAL_DIR / "bitcoin_FULL_DATASET.csv"
final_df.to_csv(out_path, index=False)

print(f"🧬 Dataset FINAL criado: {out_path}")
