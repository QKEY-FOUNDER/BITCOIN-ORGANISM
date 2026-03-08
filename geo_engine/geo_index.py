import os
import csv
from geo_engine.region_map import REGIONS


# Pasta onde a memória geográfica histórica vive
DATA_GEO_PATH = "data_geo/monthly_region_dominance"


# -----------------------------
# Time utilities
# -----------------------------

def extract_month_from_csv(csv_path):
    # Ex: data/.../bitcoin_2017_12.csv → 2017_12
    name = os.path.basename(csv_path)
    parts = name.replace(".csv", "").split("_")
    return parts[1] + "_" + parts[2]


# -----------------------------
# Historical memory
# -----------------------------

def load_historical_geo(month):
    path = os.path.join(DATA_GEO_PATH, f"{month}.csv")

    if not os.path.exists(path):
        return None

    geo = {}

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            geo[r["region"]] = float(r["dominance"])

    return geo


# -----------------------------
# Unified geographic brain
# -----------------------------

def get_geo_vector(csv_path):

    month = extract_month_from_csv(csv_path)

    # 1️⃣ Tenta memória histórica
    historical = load_historical_geo(month)
    if historical:
        return historical

    # 2️⃣ Replay histórico determinístico (sem chamadas externas)
    total_regions = len(REGIONS)

    if total_regions == 0:
        return {}

    neutral_weight = 1.0 / total_regions

    return {region: neutral_weight for region in REGIONS}
