import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

FINAL_DIR = DATA_DIR / "final"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

monthly_files = sorted(DATA_DIR.glob("bitcoin_????_??.csv"))

for csv_path in monthly_files:
    print(f"→ processar {csv_path.name}")

    df = pd.read_csv(csv_path)

    if "DominanceBTC" in df.columns:
        print("⚠️ já contém DominanceBTC — ignorado")
        continue

    raise RuntimeError(
        "Este script assume que TODOS os CSVs mensais já contêm DominanceBTC.\n"
        "A fusão diária deve acontecer ANTES deste passo."
    )

print("✓ verificação concluída (nenhuma escrita realizada)")
