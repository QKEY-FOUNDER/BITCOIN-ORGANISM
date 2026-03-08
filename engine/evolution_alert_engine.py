import json
from pathlib import Path
from datetime import datetime

BASE_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_PATH / "data"

REFLEX_FILE = DATA_PATH / "evolution_reflex_signal.json"
ALERT_FILE = DATA_PATH / "evolution_alert_log.json"


def load_reflex():

    with open(REFLEX_FILE) as f:
        return json.load(f)


def evaluate_alert(signal):

    if signal in ["Critical Expansion", "Deep Compression"]:
        level = "HIGH"

    elif signal in ["Rapid Expansion", "Rapid Contraction"]:
        level = "MEDIUM"

    else:
        level = "LOW"

    return level


def save_alert(signal, level):

    alert = {
        "timestamp": datetime.utcnow().isoformat(),
        "signal": signal,
        "alert_level": level
    }

    if ALERT_FILE.exists():

        with open(ALERT_FILE) as f:
            history = json.load(f)

    else:
        history = []

    history.append(alert)

    with open(ALERT_FILE, "w") as f:
        json.dump(history, f, indent=4)


def main():

    print("\nBitcoin Organism — Evolution Alert Engine")
    print("--------------------------------------------------")

    reflex = load_reflex()

    signal = reflex["reflex_signal"]

    level = evaluate_alert(signal)

    save_alert(signal, level)

    print("Reflex signal:", signal)
    print("Alert level:", level)

    print("Alert log updated:")
    print(ALERT_FILE)


if __name__ == "__main__":
    main()
