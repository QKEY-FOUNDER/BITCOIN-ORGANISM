import time
import subprocess
from datetime import datetime
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


INTERVAL_HOURS = 24


def run_organism():

    print("\n==================================================")
    print("BITCOIN ORGANISM — AUTONOMOUS CYCLE")
    print("Time:", datetime.utcnow())
    print("==================================================")

    subprocess.run(
        ["python3", "organism_autonomous.py"],
        cwd=BASE_PATH
    )


def main():

    print("\nBitcoin Organism Biological Clock")
    print("Cycle interval:", INTERVAL_HOURS, "hours")

    while True:

        run_organism()

        print("\nNext cycle in", INTERVAL_HOURS, "hours")
        print("--------------------------------------------------")

        time.sleep(INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    main()
