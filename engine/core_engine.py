from immune_system.organism_validator import evaluate_health
from geo_engine.geo_index import get_geo_vector
geo_vector = get_geo_vector(CSV_PATH)
from geo_engine.geo_traits import combine_geo_traits

import csv
import math
import wave
import struct

# -----------------------------
# CONFIG
# -----------------------------

CSV_PATH = "data/06_institutional_awakening_2020_2022/bitcoin_2020_01.csv"

SAMPLE_RATE = 44100
BASE_FREQ = 293.66   # D4
DNA_INTERVALS = [0, 7, 3, 0, -2, 0]

# -----------------------------
# HELPERS
# -----------------------------

def semitone_to_freq(base, semitone):
    return base * (2 ** (semitone / 12))

def normalize(x, a, b):
    if b - a == 0:
        return 0.5
    return (x - a) / (b - a)

# -----------------------------
# LOAD CSV
# -----------------------------

rows = []
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

opens  = [float(r["Open"]) for r in rows]
highs  = [float(r["High"]) for r in rows]
lows   = [float(r["Low"]) for r in rows]
closes = [float(r["Close"]) for r in rows]
vols   = [float(r["Volume"]) for r in rows]
doms   = [float(r["DominanceBTC"]) for r in rows]

vol_min, vol_max = min(vols), max(vols)
stress_raw = [h - l for h, l in zip(highs, lows)]
smin, smax = min(stress_raw), max(stress_raw)

# -----------------------------
# GEO SYSTEM
# -----------------------------

geo_vector = compute_geo_vector(CSV_PATH)
geo_traits = combine_geo_traits(geo_vector)
intraday_geo = compute_intraday_geo_vector()

geo_bpm        = geo_traits["bpm"]
geo_brightness = geo_traits["brightness"]
geo_aggression = geo_traits["harmonic_aggression"]
geo_stability  = geo_traits["stability"]

SECONDS_PER_DAY = 60.0 / geo_bpm * 8   # 8 beats per candle

# -----------------------------
# SYNTHESIS
# -----------------------------

audio = []

for i in range(len(rows)):

    energy = normalize(vols[i], vol_min, vol_max)
    direction = (closes[i] - opens[i]) / opens[i]
    stress = normalize(stress_raw[i], smin, smax)
    confidence = doms[i] / 100.0

    geo = compute_geo_dominance(CSV_PATH)
    health = evaluate_health(stress, vols[i], geo)

    # cardiac trigger from price acceleration
    if i > 0:
        price_velocity = abs(closes[i] - closes[i-1]) / closes[i-1]
    else:
        price_velocity = 0.0

    tachy = price_velocity > 0.05
    arrhythmia = price_velocity > 0.12

    amp = (0.3 + 0.7 * energy) * geo_brightness

    if health == "HEALTHY":
        gravity = 0.8 + confidence * 0.4
    elif health == "STRESSED":
        gravity = 0.6 + confidence * 0.3
    elif health == "INFECTED":
        gravity = 0.3 + confidence * 0.2
    else:
        gravity = 0.5

    pitch = max(-6, min(6, direction * 12 + geo_aggression * 6))

    samples = int(SAMPLE_RATE * SECONDS_PER_DAY)

    for n in range(samples):
        t = n / SAMPLE_RATE

        # heart rate from stress
        heart_rate = geo_bpm * (1 + stress * 2)
        if tachy:
            heart_rate *= 1.5
        if arrhythmia:
            heart_rate *= 2.5

        heartbeat = math.sin(2 * math.pi * heart_rate / 60 * t)

        if arrhythmia:
            pulse = math.sin(2 * math.pi * heart_rate / 45 * t + math.sin(t * 20))
            rhythm_gate = 1 if pulse > 0 else 0.1
        elif tachy:
            rhythm_gate = 1 if heartbeat > 0 else 0.15
        else:
            rhythm_gate = 1 if heartbeat > 0 else 0.3

        # intraday region
        hour = int((n / samples) * 24)
        hour_geo = intraday_geo.get(hour, {})
        local_weight = max(hour_geo.values()) if hour_geo else 1.0

        # rhythmic pulse driven by geopolitics
        v = 0.0
        for interval in DNA_INTERVALS:
            geo_bias = geo.get("north_america", 0.25) - geo.get("east_asia", 0.25)
            freq = semitone_to_freq(BASE_FREQ, interval + pitch + geo_bias * 4)
            freq += stress * (5 + geo_aggression * 5) * math.sin(2 * math.pi * 0.5 * t)
            v += math.sin(2 * math.pi * freq * t)

        v /= len(DNA_INTERVALS)

        life = math.sin(math.pi * n / samples)
        env = life * rhythm_gate * local_weight

        v *= env * amp * gravity
        audio.append(v)

# -----------------------------
# NORMALIZE & WRITE WAV
# -----------------------------

mx = max(abs(x) for x in audio)
audio = [x / mx for x in audio]

wav = wave.open("bitcoin_organism_jan_2020.wav", "w")
wav.setnchannels(1)
wav.setsampwidth(2)
wav.setframerate(SAMPLE_RATE)

for s in audio:
    wav.writeframes(struct.pack("h", int(s * 32767)))

wav.close()

print("Bitcoin-Organism with Geopolitical Circadian Rhythm created.")
