import pandas as pd
import json
from datetime import datetime

DATA_FILE = "data/btc_price_live.csv"
OUTPUT_FILE = "data/evolution_pulse_state.json"

print("Bitcoin Organism — Evolution Pulse Engine")
print("--------------------------------------------------")

# Load market data
df = pd.read_csv(DATA_FILE)

# Calculate returns
df["returns"] = df["price"].pct_change()

# Remove NaN
df = df.dropna()

# Calculate pulse metrics
current_pressure = df["returns"].tail(30).std()
velocity = df["returns"].tail(7).mean()
acceleration = velocity * 2

# Determine pulse state
pulse_state = "Stable"

if velocity > 0:
    pulse_state = "Accelerating Expansion"

if velocity < 0:
    pulse_state = "Contraction Phase"

# Build state dictionary
state = {
    "current_pressure": float(current_pressure),
    "velocity": float(velocity),
    "acceleration": float(acceleration),
    "pulse_state": pulse_state,
    "timestamp": str(datetime.utcnow())
}

# Save state
with open(OUTPUT_FILE, "w") as f:
    json.dump(state, f, indent=2)

print("")
print("Current pressure:", current_pressure)
print("Velocity:", velocity)
print("Acceleration:", acceleration)
print("")
print("Evolution pulse state:")
print(pulse_state)
print("")
print("Pulse state saved:")
print(OUTPUT_FILE)
