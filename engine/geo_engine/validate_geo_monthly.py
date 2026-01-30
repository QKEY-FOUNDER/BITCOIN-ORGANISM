from pathlib import Path
import pandas as pd
import sys
import re

print("🧩 GEO MONTHLY VALIDATOR — SANIDADE HISTÓRICA")
print("=" * 60)

# ---------------------------------------------------------
# ROOTS
# ---------------------------------------------------------

ENGINE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT   = ENGINE_ROOT.parents[2]

DATA_GEO = REPO_ROOT / "data_geo"
REGION_PATH   = DATA_GEO / "monthly_region_dominance"
EXCHANGE_PATH = DATA_GEO / "monthly_exchange_dominance"

# ---------------------------------------------------------
# CANONICAL REGIONS
# ---------------------------------------------------------

CANONICAL_REGIONS = {
    "north_america",
    "south_america",
    "europe",
    "east_asia",
    "south_asia",
    "middle_east",
    "africa",
    "oceania",
    "global_offshore",
}

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def valid_month_filename(name: str) -> bool:
    return re.match(r"^\d{4}_(0[1-9]|1[0-2])\.csv$", name) is not None


def validate_sum(series, tolerance=0.01):
    total = series.sum()
    return abs(total - 1.0) <= tolerance


# ---------------------------------------------------------
# VALIDATORS
# ---------------------------------------------------------

def validate_region_file(path: Path):
    df = pd.read_csv(path)

    if list(df.columns) != ["region", "weight"]:
        raise ValueError("Estrutura inválida (esperado: region, weight)")

    if df.empty:
        raise ValueError("Ficheiro vazio")

    if df["weight"].isna().any():
        raise ValueError("Weights NaN")

    if (df["weight"] < 0).any() or (df["weight"] > 1).any():
        raise ValueError("Weights fora do intervalo [0,1]")

    unknown = set(df["region"]) - CANONICAL_REGIONS
    if unknown:
        raise ValueError(f"Regiões desconhecidas: {unknown}")

    if not validate_sum(df["weight"]):
        raise ValueError("Soma dos weights ≠ 1.0")


def validate_exchange_file(path: Path):
    df = pd.read_csv(path)

    if list(df.columns) != ["exchange", "weight"]:
        raise ValueError("Estrutura inválida (esperado: exchange, weight)")

    if df.empty:
        raise ValueError("Ficheiro vazio")

    if df["weight"].isna().any():
        raise ValueError("Weights NaN")

    if (df["weight"] < 0).any() or (df["weight"] > 1).any():
        raise ValueError("Weights fora do intervalo [0,1]")

    if not validate_sum(df["weight"]):
        raise ValueError("Soma dos weights ≠ 1.0")


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

errors = 0

for folder, validator in [
    (REGION_PATH, validate_region_file),
    (EXCHANGE_PATH, validate_exchange_file),
]:
    if not folder.exists():
        print(f"⚠️ Pasta ausente: {folder}")
        continue

    for file in sorted(folder.glob("*.csv")):
        name = file.name

        print(f"🔎 Validando {folder.name}/{name} …", end=" ")

        if not valid_month_filename(name):
            print("❌ nome inválido")
            errors += 1
            continue

        year = int(name[:4])
        if year > 2025:
            print("❌ ano fora do modo memória")
            errors += 1
            continue

        try:
            validator(file)
            print("✅ OK")
        except Exception as e:
            print(f"❌ {e}")
            errors += 1

print("-" * 60)

if errors > 0:
    print(f"❌ Validação falhou ({errors} erros)")
    sys.exit(1)

print("✅ GEO histórico validado com sucesso")
