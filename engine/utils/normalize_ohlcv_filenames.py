from pathlib import Path

print("🔧 NORMALIZAR NOMES OHLCV")

BASE = Path(__file__).resolve().parents[2]
RAW_DIR = BASE / "data/raw/ohlcv"

files = list(RAW_DIR.glob("btc_ohlcv_*.csv"))

for f in files:
    name = f.name
    
    if " " in name:
        new_name = name.split(" ")[0] + ".csv"
        new_path = RAW_DIR / new_name
        
        f.rename(new_path)
        print(f"✔ Renomeado: {name} → {new_name}")

print("✅ Normalização concluída")
