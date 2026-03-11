import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.cluster import KMeans

BASE_PATH = Path(__file__).resolve().parent.parent

PRESSURE_FILE = BASE_PATH / "data" / "evolution_pressure.csv"
OUTPUT_FILE = BASE_PATH / "data" / "evolution_attractor_state.json"


def load_pressure_series():

    try:

        df = pd.read_csv(PRESSURE_FILE)

        if "pressure" not in df.columns:
            return None

        return df["pressure"].dropna().values.reshape(-1,1)

    except:

        return None


def compute_attractors(series, n_clusters=4):

    model = KMeans(n_clusters=n_clusters, random_state=42)

    model.fit(series)

    centers = model.cluster_centers_

    labels = model.labels_

    return centers.flatten(), labels


def detect_current_attractor(series, centers):

    current = series[-1][0]

    distances = [abs(current - c) for c in centers]

    idx = np.argmin(distances)

    return idx, centers[idx]


def main():

    print("")
    print("Bitcoin Organism — Evolution Attractor Engine")
    print("--------------------------------------------------")

    pressure_series = load_pressure_series()

    if pressure_series is None:

        print("Pressure series unavailable")
        return

    centers, labels = compute_attractors(pressure_series)

    attractor_id, attractor_value = detect_current_attractor(pressure_series, centers)

    print("")
    print("Detected attractors (pressure levels):")

    for i,c in enumerate(centers):

        print("Attractor",i,"→",round(float(c),4))

    print("")
    print("Current system pressure:",round(float(pressure_series[-1][0]),4))
    print("Current attractor:",attractor_id)
    print("Attractor pressure level:",round(float(attractor_value),4))

    output = {

        "current_pressure": float(pressure_series[-1][0]),
        "current_attractor": int(attractor_id),
        "attractor_pressure_level": float(attractor_value),
        "all_attractors": [float(c) for c in centers]

    }

    with open(OUTPUT_FILE,"w") as f:

        json.dump(output,f)

    print("")
    print("Attractor state saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
