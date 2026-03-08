import os
import csv
import math
from statistics import stdev, mean
from geo_engine.geo_index import get_geo_vector


def compute_entropy(distribution):
    total = sum(distribution.values())
    if total == 0:
        return 0.0

    entropy = 0.0
    for v in distribution.values():
        p = v / total
        if p > 0:
            entropy -= p * math.log(p)

    return entropy / math.log(len(distribution))


def extract_dominance(row):
    if "DominanceBTC" in row:
        return float(row["DominanceBTC"])
    if "BTC_Dominance" in row:
        return float(row["BTC_Dominance"])
    return None


def normalize(value, scale):
    return min(1.0, abs(value) * scale)


def compute_market_biometrics(csv_path):

    rows = []

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    # --------------------------------------------------
    # Verificação de dados mínimos
    # --------------------------------------------------

    if len(rows) < 5:

        return {
            "heartbeat_variability": None,
            "arrhythmia_index": None,
            "geo_entropy": None,
            "volatility_resonance": None,
            "structural_tension": None,
            "dominance_variability": None,
            "dominance_shift": None,
            "dominance_pressure": None
        }

    closes = [float(r["Close"]) for r in rows]
    highs  = [float(r["High"]) for r in rows]
    lows   = [float(r["Low"]) for r in rows]
    vols   = [float(r["Volume"]) for r in rows]

    # -----------------------------
    # Dominance
    # -----------------------------

    dominance_values = [
        extract_dominance(r) for r in rows
        if extract_dominance(r) is not None
    ]

    if len(dominance_values) > 1:
        dominance_variability = stdev(dominance_values)
        dominance_shift = dominance_values[-1] - dominance_values[0]
    else:
        dominance_variability = 0.0
        dominance_shift = 0.0

    dominance_pressure = normalize(dominance_shift / 100.0, 5)

    # -----------------------------
    # Heartbeat variability
    # -----------------------------

    velocities = []
    for i in range(1, len(closes)):
        v = abs(closes[i] - closes[i-1]) / closes[i-1]
        velocities.append(v)

    hbv = stdev(velocities) if len(velocities) > 1 else 0.0

    # -----------------------------
    # Arrhythmia index
    # -----------------------------

    threshold = mean(velocities) * 2 if velocities else 0.0
    arrhythmia_events = sum(1 for v in velocities if v > threshold)
    arrhythmia_index = arrhythmia_events / len(velocities) if velocities else 0.0

    # -----------------------------
    # Geo entropy
    # -----------------------------

    geo_vector = get_geo_vector(csv_path)
    geo_entropy = compute_entropy(geo_vector)

    # -----------------------------
    # Volatility resonance
    # -----------------------------

    stress = [h - l for h, l in zip(highs, lows)]

    if len(stress) > 1:
        avg_stress = mean(stress)
        avg_vol = mean(vols)

        numerator = sum((s-avg_stress)*(v-avg_vol) for s, v in zip(stress, vols))
        denom1 = math.sqrt(sum((s-avg_stress)**2 for s in stress))
        denom2 = math.sqrt(sum((v-avg_vol)**2 for v in vols))

        volatility_resonance = numerator / (denom1 * denom2) if denom1 and denom2 else 0.0
    else:
        volatility_resonance = 0.0

        # -----------------------------
    # Structural tension (modelo corrigido)
    # -----------------------------

    tension_raw = (
        hbv * 4 +
        arrhythmia_index * 3 +
        abs(volatility_resonance) * 2 +
        dominance_pressure * 2
    )

    # compressão suave (função logística simples)
    structural_tension = tension_raw / (1 + tension_raw)

    return {
        "heartbeat_variability": round(hbv, 6),
        "arrhythmia_index": round(arrhythmia_index, 6),
        "geo_entropy": round(geo_entropy, 6),
        "volatility_resonance": round(volatility_resonance, 6),
        "structural_tension": round(structural_tension, 6),
        "dominance_variability": round(dominance_variability, 6),
        "dominance_shift": round(dominance_shift, 6),
        "dominance_pressure": round(dominance_pressure, 6)
    }
