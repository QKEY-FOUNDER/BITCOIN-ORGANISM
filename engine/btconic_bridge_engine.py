import json
import csv
import subprocess
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PROFILE_PATH = DATA_PATH / "btconic_music_profile.json"
CSV_PATH = DATA_PATH / "evolution_pressure.csv"


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
        return {
            "tempo": 70,
            "mode": "major",
            "density": "low",
            "rhythm": "steady"
        }

    if regime == "Compression":
        return {
            "tempo": 85,
            "mode": "minor",
            "density": "medium",
            "rhythm": "pulsing"
        }

    if regime == "Expansion":
        return {
            "tempo": 110,
            "mode": "major",
            "density": "high",
            "rhythm": "driving"
        }

    return {
        "tempo": 130,
        "mode": "dissonant",
        "density": "chaotic",
        "rhythm": "irregular"
    }


def get_latest_state():

    records = []

    with open(CSV_PATH) as f:

        reader = csv.DictReader(f)

        for row in reader:

            month = row["month"]
            pressure = float(row["pressure"])

            records.append((month, pressure))

    records.sort()

    return records[-1]


def save_profile(profile):

    with open(PROFILE_PATH, "w") as f:

        json.dump(profile, f, indent=4)


def run_btconic():

    print("\nLaunching BTCONIC Composer...\n")

    subprocess.run(
        ["python3", "-m", "engine.run_music"],
        cwd=BASE_PATH.parent / "BTConic-MUSIC-V2"
    )


def main():

    print("\nBitcoin Organism → BTCONIC Bridge")
    print("--------------------------------------------------")

    month, pressure = get_latest_state()

    regime = classify_regime(pressure)

    profile = music_profile(regime)

    print("Latest month:", month)
    print("Evolution pressure:", pressure)
    print("Regime:", regime)

    save_profile(profile)

    print("\nMusic profile exported:")
    print(PROFILE_PATH)

    run_btconic()


if __name__ == "__main__":
    main()
