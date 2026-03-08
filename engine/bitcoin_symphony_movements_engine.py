import csv
import json
import subprocess
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

PRESSURE_CSV = DATA_PATH / "evolution_pressure.csv"
PROFILE_PATH = DATA_PATH / "btconic_music_profile.json"


HALVING_CYCLES = [
    ("Genesis", 2010, 2012),
    ("Early Expansion", 2013, 2016),
    ("Global Discovery", 2017, 2020),
    ("Institutional Awakening", 2021, 2024),
    ("Global Monetary Layer", 2025, 2030)
]


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
        return {"tempo":70,"mode":"major","density":"low"}

    if regime == "Compression":
        return {"tempo":85,"mode":"minor","density":"medium"}

    if regime == "Expansion":
        return {"tempo":110,"mode":"major","density":"high"}

    return {"tempo":130,"mode":"dissonant","density":"chaotic"}


def load_series():

    series = []

    with open(PRESSURE_CSV) as f:

        reader = csv.DictReader(f)

        for row in reader:

            month = row["month"]
            pressure = float(row["pressure"])

            year = int(month.split("_")[1])

            series.append((month, year, pressure))

    return series


def export_profile(profile):

    with open(PROFILE_PATH,"w") as f:

        json.dump(profile,f,indent=4)


def run_btconic():

    subprocess.run(
        ["python3","-m","engine.run_music"],
        cwd=BASE_PATH.parent/"BTConic-MUSIC-V2",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def main():

    print("\nBitcoin Symphony — Movements")
    print("--------------------------------------------------")

    series = load_series()

    for name,start,end in HALVING_CYCLES:

        print("\nMovement:",name)
        print(start,"→",end)
        print("")

        for month,year,pressure in series:

            if year < start or year > end:
                continue

            regime = classify_regime(pressure)

            profile = music_profile(regime)

            export_profile(profile)

            print(month,"→",regime)

            run_btconic()

    print("\nBitcoin Symphony complete.")


if __name__ == "__main__":
    main()
