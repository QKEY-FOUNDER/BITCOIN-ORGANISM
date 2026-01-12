import csv
import math
import wave
import struct

# -----------------------------
# CONFIG
# -----------------------------
CSV_PATH = "../data/06_institutional_awakening_2020_2022/bitcoin_2020_01.csv"
SAMPLE_RATE = 44100
SECONDS_PER_DAY = 2.0
BASE_FREQ = 293.66  # D4

DNA_INTERVALS = [0, 7, 3, 0, -2, 0]

# -----------------------------
# HELPERS
# -----------------------------
def semitone_to_freq(base, semitone):
    return base * (2 ** (semitone / 12))

def normalize(x, min_x, max_x):
    if max_x - min_x == 0:
        return 0.5
    return (x - min_x) / (max_x - min_x)

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
lows = [float(r["Low"]) for r in rows]
closes = [float(r["Close"]) for r in rows]
volumes = [float(r["Volume"]) for r in rows]
dominance = [float(r["DominanceBTC"]) for r in rows]

vol_min, vol_max = min(volumes), max(volumes)
stress_vals = [highs[i] - lows[i] for i in range(len(rows))]
stress_min, stress_max = min(stress_vals), max(stress_vals)

# -----------------------------
# SOUND
# -----------------------------
audio = []

for i in range(len(rows)):
    energy = normalize(volumes[i], vol_min, vol_max)
    direction = (closes[i] - opens[i]) / opens[i]
    stress = normalize(stress_vals[i], stress_min, stress_max)
    confidence = dominance[i] / 100.0

    duration = SECONDS_PER_DAY
    samples = int(SAMPLE_RATE * duration)

    pitch_shift = max(-6, min(6, direction * 12))
    detune = stress * 5
    amp = 0.3 + 0.7 * energy
    gravity = 0.5 + confidence * 0.5

    for n in range(samples):
        t = n / SAMPLE_RATE
        sample = 0.0

        for interval in DNA_INTERVALS:
            freq = semitone_to_freq(BASE_FREQ, interval + pitch_shift)
            freq += detune * math.sin(2 * math.pi * 0.5 * t)
            sample += math.sin(2 * math.pi * freq * t)

        sample /= len(DNA_INTERVALS)

        envelope = math.sin(math.pi * (n / samples))
        sample *= envelope * amp * gravity

        audio.append(sample)

# -----------------------------
# NORMALIZE
# -----------------------------
max_amp = max(abs(x) for x in audio)
audio = [x / max_amp for x in audio]

# -----------------------------
# WRITE WAV
# -----------------------------
with wave.open("bitcoin_organism_jan_2020.wav", "w") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)

    for s in audio:
        wf.writeframes(struct.pack("<h", int(s * 32767)))

print("Bitcoin-Organism January 2020 voice generated.")
