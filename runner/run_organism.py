import os
import subprocess
import sys
import json
from pathlib import Path

from engine.metrics_engine import compute_market_biometrics

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "data")

# -------------------------------------------------------
# Execute core engine (WAV generation)
# -------------------------------------------------------

def run_month(csv_file):
    print("🧬 Processing:", csv_file)

    env = os.environ.copy()
    env["CSV_PATH"] = csv_file

    subprocess.run(
        [sys.executable, "-m", "engine.core_engine"],
        env=env,
        cwd=BASE_PATH
    )

# -------------------------------------------------------
# Export biometrics
# -------------------------------------------------------

def export_metrics(csv_file):

    metrics = compute_market_biometrics(csv_file)

    metrics_dir = Path("data/organism_metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)

    month_name = os.path.basename(csv_file).replace(".csv", "")
    monthly_path = metrics_dir / f"{month_name}_metrics.json"
    latest_path = metrics_dir / "latest_metrics.json"

    with open(monthly_path, "w") as f:
        json.dump(metrics, f, indent=2)

    with open(latest_path, "w") as f:
        json.dump(metrics, f, indent=2)

# -------------------------------------------------------
# Walk data tree (clean)
# -------------------------------------------------------

def walk_data_tree():

    files = []

    for root, dirs, filenames in os.walk(DATA_PATH):

        # Ignorar pastas indesejadas
        if "MIRROR" in root or "data_geo" in root:
            continue

        for f in sorted(filenames):
            if f.endswith(".csv") and f.startswith("bitcoin_"):
                files.append(os.path.join(root, f))

    return sorted(files)

# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":

    print("🌍 Bitcoin Organism Awakening")

    files = walk_data_tree()

    print(f"Total files found: {len(files)}")

    for csv_file in files:
        run_month(csv_file)
        export_metrics(csv_file)

    print("✨ Evolution complete. The organism has spoken.")
