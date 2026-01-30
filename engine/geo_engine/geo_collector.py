from engine.utils.hardening import silence_known_warnings
silence_known_warnings()

from pathlib import Path
import pandas as pd
import sys

# =========================================================
# GEO COLLECTOR — MONTHLY (PROPOSAL MODE)
# =========================================================
print("🌍 GEO COLLECTOR — MODO PROPOSTA (READ-ONLY)")
print("=" * 55)

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_GEO_DIR = PROJECT_ROOT / "data_geo"
EXCHANGE_DOM_DIR = DATA_GEO_DIR / "monthly_exchange_dominance"
REGION_DOM_DIR   = DATA_GEO_DIR / "monthly_region_dominance"
MAP_FILE         = DATA_GEO_DIR / "exchange_region_map.csv"

PROPOSALS_DIR = DATA_GEO_DIR / "proposals"
PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# UTILITIES
# =========================================================
def resolve_target_month(arg):
    if arg:
        return arg
    print("❌ Mês alvo não fornecido (formato: YYYY_MM)")
    sys.exit(1)

def load_exchange_region_map():
    if not MAP_FILE.exists():
        print(f"❌ exchange_region_map não encontrado: {MAP_FILE}")
        sys.exit(1)
    return pd.read_csv(MAP_FILE)

def load_monthly_evidence(month):
    """
    Placeholder:
    Aqui entram futuramente fontes semi-automáticas:
    - volumes por exchange
    - eventos regulatórios
    - bans / colapsos
    """
    print(f"📥 Evidência externa ainda não integrada para {month}")
    return pd.DataFrame()

# =========================================================
# CORE LOGIC
# =========================================================
def build_exchange_dominance(month, exchange_map, evidence):
    """
    Gera PROPOSTA de dominância por exchange.
    Atualmente: estrutura vazia + validação de formato.
    """
    df = exchange_map[["exchange"]].drop_duplicates().copy()
    df["weight"] = None  # a ser preenchido manualmente
    df["month"] = month
    return df[["month", "exchange", "weight"]]

def propagate_to_regions(exchange_df, exchange_map):
    merged = exchange_df.merge(exchange_map, on="exchange", how="left")
    region_df = (
        merged.groupby("region", dropna=False)["weight"]
        .sum()
        .reset_index()
    )
    region_df["month"] = exchange_df["month"].iloc[0]
    return region_df[["month", "region", "weight"]]

def write_proposals(month, exchange_df, region_df):
    ex_file = PROPOSALS_DIR / f"exchange_dominance_{month}.csv"
    rg_file = PROPOSALS_DIR / f"region_dominance_{month}.csv"

    exchange_df.to_csv(ex_file, index=False)
    region_df.to_csv(rg_file, index=False)

    print("📝 Propostas GEO geradas:")
    print(f" • {ex_file}")
    print(f" • {rg_file}")

# =========================================================
# MAIN
# =========================================================
def main(arg):
    month = resolve_target_month(arg)
    print(f"📆 Mês alvo: {month}")

    exchange_map = load_exchange_region_map()
    evidence = load_monthly_evidence(month)

    exchange_df = build_exchange_dominance(month, exchange_map, evidence)
    region_df   = propagate_to_regions(exchange_df, exchange_map)

    write_proposals(month, exchange_df, region_df)

    print("🧠 GEO Collector executado em modo observação.")
    print("Nenhuma escrita canónica foi feita.")

# =========================================================
if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
