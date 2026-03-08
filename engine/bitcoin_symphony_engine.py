import csv
import json
import subprocess
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"
PROFILE_PATH = DATA_PATH / "btconic_music_profile.json"


def classify_regime(p):
    if p < 1.5:
        return "Equilibrium"
    if p < 2.2:
        return "Compression"
    if p < 3.0:
        return "Expansion"
    return "Instability"


def music_profile(regime):
    if regime == "Equilibrium":
        return {"tempo": 70, "mode": "major", "density": "low"}
    if regime == "Compression":
        return {"tempo": 85, "mode": "minor", "density": "medium"}
    if regime == "Expansion":
        return {"tempo": 110, "mode": "major", "density": "high"}
    return {"tempo": 130, "mode": "dissonant", "density": "chaotic"}


def load_pressure_series():
    series = []

    with open(PRESSURE_CSV) as f:
        reader = csv.DictReader(f)

        for row in reader:
            month = row["month"]
            pressure = float(row["pressure"])
            series.append((month, pressure))

    return series


def export_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)


def run_btconic():
    subprocess.run(
        ["python3", "-m", "engine.run_music"],
        cwd=BASE_PATH.parent / "BTConic-MUSIC-V2"
    )


def main():

    print("\nBitcoin Symphony Engine")
    print("--------------------------------------------------")

    series = load_pressure_series()

    print("Months in dataset:", len(series))
    print("Generating musical evolution...\n")

    for month, pressure in series:

        regime = classify_regime(pressure)

        profile = music_profile(regime)

        export_profile(profile)

        print(month, "->", regime)

        run_btconic()

    print("\nBitcoin Symphony complete.")


if __name__ == "__main__":
    main()
