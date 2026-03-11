import json
import pandas as pd
import streamlit as st
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent
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


st.set_page_config(page_title="Bitcoin Organism Observatory", layout="wide")

st.title("🧬 BITCOIN ORGANISM OBSERVATORY")

data = {k: load_json(v) for k, v in FILES.items()}

observatory = data["observatory"]
pulse = data["pulse"]
brain = data["brain"]
sync = data["sync"]
cycle = data["cycle"]

col1, col2, col3, col4 = st.columns(4)

if observatory:
    col1.metric("Evolution Stage", observatory.get("evolution_stage"))

if pulse:
    col2.metric("Pulse State", pulse.get("pulse_state"))

if brain:
    col3.metric("Model State", brain.get("model_state"))

if cycle:
    col4.metric("Cycle Signal", cycle.get("cycle_signal"))

st.subheader("Macro Synchronization")

if sync:
    st.write(sync.get("synchronization_state"))

st.subheader("Evolution Pressure Timeline")

try:
    df = pd.read_csv(PRESSURE_FILE)
    st.line_chart(df["pressure"])
except:
    st.write("Pressure data not available")

st.subheader("System Data")

st.json({
    "observatory": observatory,
    "pulse": pulse,
    "brain": brain,
    "cycle": cycle
})
