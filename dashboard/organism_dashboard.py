import json
import pandas as pd
import streamlit as st
import os
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

HEARTBEAT_FILE = (
    DATA_PATH
    / "07_Reconfiguracao_Global_2022_Plus"
    / "data"
    / "output"
    / "heartbeat"
    / "cron.log"
)


def load_json(file):
    try:
        with open(DATA_PATH / file) as f:
            return json.load(f)
    except:
        return None


def get_last_heartbeat():
    try:
        with open(HEARTBEAT_FILE) as f:
            lines = f.readlines()
            return lines[-1]
    except:
        return None


st.set_page_config(
    page_title="Bitcoin Organism Observatory",
    layout="wide"
)

st.title("🧬 BITCOIN ORGANISM OBSERVATORY")

data = {k: load_json(v) for k, v in FILES.items()}

observatory = data["observatory"]
pulse = data["pulse"]
brain = data["brain"]
sync = data["sync"]
cycle = data["cycle"]


# ------------------------------
# Evolution Radar
# ------------------------------

st.subheader("Evolution Radar")

col1, col2, col3, col4 = st.columns(4)

if observatory:
    col1.metric("Evolution Stage", observatory.get("evolution_stage"))

if pulse:
    col2.metric("Pulse State", pulse.get("pulse_state"))

if brain:
    col3.metric("Model State", brain.get("model_state"))

if cycle:
    col4.metric("Cycle Phase", cycle.get("cycle_signal"))


# ------------------------------
# Market Regime
# ------------------------------

st.subheader("Market Regime")

if observatory:
    regime = observatory.get("evolution_stage")

    if regime:
        if "Expansion" in regime:
            st.success(f"Regime: {regime}")

        elif "Compression" in regime:
            st.warning(f"Regime: {regime}")

        elif "Instability" in regime:
            st.error(f"Regime: {regime}")

        else:
            st.info(f"Regime: {regime}")


# ------------------------------
# Macro Synchronization
# ------------------------------

st.subheader("Macro Synchronization")

if sync:
    sync_state = sync.get("synchronization_state")

    if sync_state == "aligned":
        st.success("Global synchronization detected")

    elif sync_state == "neutral":
        st.info("Global systems neutral")

    else:
        st.warning("Macro misalignment detected")


# ------------------------------
# Evolution Pressure Timeline
# ------------------------------

st.subheader("Evolution Pressure Timeline")

try:
    df = pd.read_csv(PRESSURE_FILE)

    if "month" in df.columns:
        st.line_chart(df.set_index("month")["pressure"])
    else:
        st.line_chart(df["pressure"])

except:
    st.write("Pressure data not available")


# ------------------------------
# Evolution Phase Map
# ------------------------------

st.subheader("Evolution Phase Map")

try:
    df = pd.read_csv(PRESSURE_FILE)

    if "tension" in df.columns:
        st.scatter_chart(
            df,
            x="tension",
            y="pressure"
        )
    else:
        st.write("Tension data not available")

except:
    st.write("Phase map data not available")


# ------------------------------
# Organism Heartbeat
# ------------------------------

st.subheader("Organism Heartbeat")

heartbeat = get_last_heartbeat()

if heartbeat:
    st.code(heartbeat)
else:
    st.write("Heartbeat not detected")


# ------------------------------
# Mission Control
# ------------------------------

st.subheader("Organism Mission Control")

colA, colB, colC = st.columns(3)

with colA:

    if st.button("Run Full Organism"):
        os.system("./run_bitcoin_organism.sh")
        st.success("Organism cycle executed")


with colB:

    if st.button("Run Physiology Engine"):
        os.system("python -m engine.physiology_generator_engine")
        st.success("Physiology updated")


with colC:

    if st.button("Run Evolution Engine"):
        os.system("python -m engine.evolution_pressure_engine")
        st.success("Evolution recalculated")


# ------------------------------
# System Data
# ------------------------------

st.subheader("System Data")

st.json({
    "observatory": observatory,
    "pulse": pulse,
    "brain": brain,
    "cycle": cycle
})
