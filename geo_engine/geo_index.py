import csv
from datetime import datetime
from region_map import REGIONS

def hour_from_timestamp(ts):
    if isinstance(ts, str):
        # tenta ISO, senão assume YYYY-MM-DD
        try:
            dt = datetime.fromisoformat(ts)
        except:
            dt = datetime.strptime(ts, "%Y-%m-%d")
    else:
        dt = datetime.utcfromtimestamp(ts)
    return dt.hour

def hour_overlap(hour, region_hours):
    start, end = region_hours

    if start <= end:
        return 1.0 if start <= hour < end else 0.0
    else:
        # janela que cruza a meia-noite
        return 1.0 if hour >= start or hour < end else 0.0

def compute_geo_dominance(csv_path):
    scores = {r: 0.0 for r in REGIONS}

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row["Date"]
            volume = float(row["Volume"])

            hour = hour_from_timestamp(ts)

            for region, meta in REGIONS.items():
                overlap = hour_overlap(hour, meta["hours"])
                scores[region] += volume * overlap

    total = sum(scores.values())
    if total == 0:
        return scores

    return {r: scores[r] / total for r in scores}
