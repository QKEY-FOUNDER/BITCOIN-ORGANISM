import os
import json
from pathlib import Path
from engine.metrics_engine import compute_market_biometrics

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "data")

metrics_dir = Path("data/organism_metrics")
metrics_dir.mkdir(parents=True, exist_ok=True)

def walk_data_tree():
    files = []

    for root, dirs, filenames in os.walk(DATA_PATH):
        if "MIRROR" in root or "data_geo" in root:
            continue

        for f in filenames:
            if f.endswith(".csv") and f.startswith("bitcoin_"):
                files.append(os.path.join(root, f))

    return sorted(files)


if __name__ == "__main__":

    files = walk_data_tree()
    print(f"Building metrics for {len(files)} months")

    for csv_file in files:

        metrics = compute_market_biometrics(csv_file)

        month_name = os.path.basename(csv_file).replace(".csv", "")
        monthly_path = metrics_dir / f"{month_name}_metrics.json"
        latest_path = metrics_dir / "latest_metrics.json"

        with open(monthly_path, "w") as f:
            json.dump(metrics, f, indent=2)

        with open(latest_path, "w") as f:
            json.dump(metrics, f, indent=2)

        print("✔ Metrics:", month_name)

    print("All historical metrics built.")
