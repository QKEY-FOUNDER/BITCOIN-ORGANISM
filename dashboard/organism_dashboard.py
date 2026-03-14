import json
import pandas as pd
import streamlit as st
import os
from pathlib import Path
import matplotlib.pyplot as plt

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

HEARTBEAT_DIR = (
    DATA_PATH
    / "07_Reconfiguracao_Global_2022_Plus"
    / "data"
    / "output"
    / "heartbeat"
)

def load_json(file):
    try:
        with open(DATA_PATH / file) as f:
            return json.load(f)
    except:
        return None

def get_latest_heartbeat():

    try:

        files = list(HEARTBEAT_DIR.glob("*.json"))

        if not files:
            return None

        latest = sorted(files)[-1]

        with open(latest) as f:
            data = json.load(f)

        return data

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


# EVOLUTION RADAR

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


# MARKET REGIME

st.subheader("Market Regime")

if observatory:

    regime = observatory.get("evolution_stage")

    if regime and "Expansion" in regime:
        st.success(f"Regime: {regime}")

    elif regime and "Compression" in regime:
        st.warning(f"Regime: {regime}")

    elif regime and "Instability" in regime:
        st.error(f"Regime: {regime}")

    else:
        st.info(f"Regime: {regime}")


# MACRO SYNCHRONIZATION

st.subheader("Macro Synchronization")

if sync:

    sync_state = sync.get("synchronization_state")

    if sync_state == "aligned":
        st.success("Global synchronization detected")

    elif sync_state == "neutral":
        st.info("Global systems neutral")

    else:
        st.warning("Macro misalignment detected")


# EVOLUTION PRESSURE TIMELINE

st.subheader("Evolution Pressure Timeline")

try:

    df = pd.read_csv(PRESSURE_FILE)

    df = df.sort_values("month")

    window = 96
    df_recent = df.tail(window)

    st.line_chart(df_recent.set_index("month")["pressure"])

    last_two = df.tail(2)

    colA, colB = st.columns(2)

    colA.metric(
        last_two.iloc[0]["month"],
        round(last_two.iloc[0]["pressure"],3)
    )

    colB.metric(
        last_two.iloc[1]["month"],
        round(last_two.iloc[1]["pressure"],3)
    )

except:

    st.write("Pressure data not available")


# EVOLUTION PHASE MAP

st.subheader("Evolution Phase Map")

try:

    df = pd.read_csv(PRESSURE_FILE)

    fig, ax = plt.subplots(figsize=(9,4))

    # REGIME ZONES

    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.35)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.35)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.35)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.35)

    ax.scatter(
        df["tension"],
        df["pressure"],
        s=25,
        alpha=0.4
    )

    recent = df.tail(6)

    ax.plot(
        recent["tension"],
        recent["pressure"],
        linewidth=2
    )

    current = df.iloc[-1]
    prev = df.iloc[-2]

    ax.scatter(
        current["tension"],
        current["pressure"],
        s=220
    )

    dx = current["tension"] - prev["tension"]
    dy = current["pressure"] - prev["pressure"]

    ax.arrow(
        prev["tension"],
        prev["pressure"],
        dx,
        dy,
        head_width=0.02,
        length_includes_head=True
    )

    ax.set_xlabel("Tension")
    ax.set_ylabel("Pressure")

    ax.set_title("Market Evolution Phase Space")

    st.pyplot(fig)

    st.success(
        f"Current Position → Tension {round(current['tension'],3)} | Pressure {round(current['pressure'],3)}"
    )

except:

    st.write("Phase map data not available")


# ORGANISM HEARTBEAT

st.subheader("Organism Heartbeat")

heartbeat = get_latest_heartbeat()

if heartbeat:

    st.success("Heartbeat detected")

    st.json(heartbeat)

else:

    st.write("Heartbeat not detected")


# MISSION CONTROL

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


# SYSTEM DATA

st.subheader("System Data")

st.json({
    "observatory": observatory,
    "pulse": pulse,
    "brain": brain,
    "cycle": cycle
})
