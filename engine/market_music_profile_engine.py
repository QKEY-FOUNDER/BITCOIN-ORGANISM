import csv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

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


def load_latest_state():

    records = []

    with open(CSV_PATH) as f:

        reader = csv.DictReader(f)

        for row in reader:

            month = row["month"]
            pressure = float(row["pressure"])

            records.append((month, pressure))

    records.sort()

    return records[-1]


def main():

    print("\nBitcoin Organism → Music Translator")
    print("--------------------------------------------------")

    month, pressure = load_latest_state()

    regime = classify_regime(pressure)

    profile = music_profile(regime)

    print("Latest month:", month)
    print("Evolution pressure:", pressure)
    print("Market regime:", regime)

    print("\nGenerated music profile:")

    for k, v in profile.items():
        print(k, ":", v)


if __name__ == "__main__":
    main()
