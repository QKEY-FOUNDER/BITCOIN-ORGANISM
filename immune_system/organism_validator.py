import csv
from datetime import datetime

# -------------------------------
# Evolutionary Phases (extracted from evolutionary_phases.md)
# -------------------------------

PHASES = [
    ("2009-01-01", "2011-12-31", "genesis", 0.90),
    ("2012-01-01", "2013-12-31", "discovery", 0.75),
    ("2014-01-01", "2016-12-31", "ideological_war", 0.50),
    ("2017-01-01", "2017-12-31", "mass_adoption", 1.20),
    ("2018-01-01", "2020-03-31", "trauma_maturity", 0.40),
    ("2020-04-01", "2022-12-31", "institutional_awakening", 0.60),
    ("2023-01-01", "2100-01-01", "regenerative_cycle", 0.70),
]

# volatility tolerance per phase
VOLATILITY_LIMIT = {
    "genesis": 0.30,
    "discovery": 0.25,
    "ideological_war": 0.15,
    "mass_adoption": 0.40,
    "trauma_maturity": 0.12,
    "institutional_awakening": 0.18,
    "regenerative_cycle": 0.20,
}

# -------------------------------
# Helpers
# -------------------------------

def get_phase(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    for start, end, name, metabolism in PHASES:
        s = datetime.strptime(start, "%Y-%m-%d")
        e = datetime.strptime(end, "%Y-%m-%d")
        if s <= d <= e:
            return name, metabolism
    return "unknown", 0.5


# -------------------------------
# Immune Scan
# -------------------------------

def scan_csv(csv_path):
    candles = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            candles.append({
                "date": row["Date"],
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"]),
            })

    return candles


def validate_organism(csv_path):
    candles = scan_csv(csv_path)

    if len(candles) < 5:
        return "DATA_TOO_SMALL"

    anomalies = 0

    for c in candles:
        phase, metabolism = get_phase(c["date"])
        vol_limit = VOLATILITY_LIMIT[phase]

        price_range = (c["high"] - c["low"]) / c["open"]

        if price_range > vol_limit:
            anomalies += 1

    anomaly_ratio = anomalies / len(candles)

    if anomaly_ratio > 0.35:
        return "INFECTED"
    elif anomaly_ratio > 0.15:
        return "STRESSED"
    else:
        return "HEALTHY"


# -------------------------------
# Command line run
# -------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python organism_validator.py <csv_file>")
        exit()

    csv_file = sys.argv[1]

    status = validate_organism(csv_file)

    print("Bitcoin Organism Immune Scan")
    print("---------------------------")
    print("File:", csv_file)
    print("Status:", status)
