import csv
import math
import wave
import struct

# -----------------------------
# CONFIG
# -----------------------------

CSV_PATH = "data/06_institutional_awakening_2020_2022/bitcoin_2020_01.csv"

SAMPLE_RATE = 44100
SECONDS_PER_DAY = 2.0
BASE_FREQ = 293.66  # D4 (Ré menor)

# Bitcoin DNA: D – A – F – D – C – D
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

opens = [float(r["Open"]) for r in rows]
highs = [float(r["High"]) for r in rows]
lows  = [float(r["Low"]) for r in rows]
closes= [float(r["Close"]) for r in rows]
vols  = [float(r["Volume"]) for r in rows]
doms  = [float(r["DominanceBTC"]) for r in rows]

vol_min, vol_max = min(vols), max(vols)
stress_raw = [h - l for h, l in zip(highs, lows)]
smin, smax = min(stress_raw), max(stress_raw)

# -----------------------------
# SYNTHESIS
# -----------------------------

audio = []

for i in range(len(rows)):

    energy = normalize(vols[i], vol_min, vol_max)
    direction = (closes[i] - opens[i]) / opens[i]
    stress = normalize(stress_raw[i], smin, smax)
    confidence = doms[i] / 100.0

    amp = 0.3 + 0.7 * energy
    gravity = 0.5 + confidence * 0.5
    pitch = max(-6, min(6, direction * 12))

    samples = int(SAMPLE_RATE * SECONDS_PER_DAY)

    for n in range(samples):
        t = n / SAMPLE_RATE
        v = 0.0

        for interval in DNA_INTERVALS:
            freq = semitone_to_freq(BASE_FREQ, interval + pitch)
            freq += stress * 5 * math.sin(2 * math.pi * 0.5 * t)
            v += math.sin(2 * math.pi * freq * t)

        v /= len(DNA_INTERVALS)

        envelope = math.sin(math.pi * n / samples)
        v *= envelope * amp * gravity

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

print("Bitcoin Organism voice created: bitcoin_organism_jan_2020.wav")
