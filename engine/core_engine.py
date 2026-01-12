import csv
import numpy as np
from scipy.io.wavfile import write

# -----------------------------
# CONFIG
# -----------------------------
CSV_PATH = "../data/06_institutional_awakening_2020_2022/bitcoin_2020_01.csv"
SAMPLE_RATE = 44100
SECONDS_PER_DAY = 2.0   # each candle becomes 2 seconds of sound
BASE_FREQ = 293.66     # D4 = Ré menor

# Bitcoin Voice DNA (D – A – F – D – C – D)
DNA_INTERVALS = [0, 7, 3, 0, -2, 0]  # semitone offsets relative to D

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
# LOAD DATA
# -----------------------------
rows = []
with open(CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

# extract series
opens = np.array([float(r["Open"]) for r in rows])
highs = np.array([float(r["High"]) for r in rows])
lows = np.array([float(r["Low"]) for r in rows])
closes = np.array([float(r["Close"]) for r in rows])
volumes = np.array([float(r["Volume"]) for r in rows])
dominance = np.array([float(r["DominanceBTC"]) for r in rows])

# ranges
vol_min, vol_max = volumes.min(), volumes.max()
stress_min, stress_max = (highs - lows).min(), (highs - lows).max()

# -----------------------------
# SOUND BUFFER
# -----------------------------
audio = []

for i in range(len(rows)):
    # ---- STATE MODEL ----
    energy = normalize(volumes[i], vol_min, vol_max)
    direction = (closes[i] - opens[i]) / opens[i]
    stress = normalize(highs[i] - lows[i], stress_min, stress_max)
    confidence = dominance[i] / 100.0

    # ---- MAP TO SOUND ----
    duration = SECONDS_PER_DAY
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    # pitch movement from direction
    pitch_shift = np.clip(direction * 12, -6, 6)

    # harmonic tension from stress
    detune = stress * 5

    # volume from energy
    amp = 0.3 + 0.7 * energy

    # harmonic gravity from confidence
    gravity = 0.5 + confidence * 0.5

    day_wave = np.zeros_like(t)

    # apply Bitcoin DNA motif
    for k, interval in enumerate(DNA_INTERVALS):
        freq = semitone_to_freq(BASE_FREQ, interval + pitch_shift)
        freq += detune * np.sin(2 * np.pi * 0.5 * t)
        wave = np.sin(2 * np.pi * freq * t)
        day_wave += wave

    day_wave = day_wave / len(DNA_INTERVALS)

    # envelope
    envelope = np.sin(np.pi * np.linspace(0, 1, len(t)))
    day_wave *= envelope

    # apply amplitude and gravity
    day_wave *= amp * gravity

    audio.extend(day_wave)

# -----------------------------
# NORMALIZE & SAVE
# -----------------------------
audio = np.array(audio)
audio /= np.max(np.abs(audio))

write("bitcoin_organism_jan_2020.wav", SAMPLE_RATE, audio.astype(np.float32))

print("Bitcoin-Organism January 2020 voice generated: bitcoin_organism_jan_2020.wav")
