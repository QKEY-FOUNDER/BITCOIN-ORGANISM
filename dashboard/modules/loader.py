import json
import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_PATH / "data"

FILES = {
    "observatory": "evolution_observatory_state.json",
    "pulse": "evolution_pulse_state.json",
    "brain": "evolution_brain_state.json",
    "sync": "global_evolution_synchronization.json",
    "cycle": "cycle_genesis_state.json"
}

PRESSURE_FILE = DATA_PATH / "evolution_pressure.csv"


def load_json(file):

    try:
        with open(DATA_PATH / file) as f:
            return json.load(f)

    except:
        return None


def load_system_state():

    state = {}

    for key, file in FILES.items():
        state[key] = load_json(file)

    return state


def load_pressure():

    try:

        df = pd.read_csv(PRESSURE_FILE)

        df["date"] = (
            df["month"]
            .str.replace("bitcoin_", "", regex=False)
        )

        df["date"] = pd.to_datetime(df["date"], format="%Y_%m", errors="coerce")

        df = df.dropna(subset=["date"])

        df = df.sort_values("date")

        return df

    except Exception as e:

        print("PRESSURE LOAD ERROR:", e)
        return None
