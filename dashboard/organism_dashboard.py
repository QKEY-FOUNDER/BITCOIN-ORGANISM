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

        df = pd.read_csv(PRESSURE_FILE)
        df = df.sort_values("month")

        last_month = df.iloc[-1]["month"]
        month_str = last_month.replace("bitcoin_", "")

        year = month_str.split("_")[0]
        month = month_str.split("_")[1]

        market_date = f"{year}-{month}-01"

        if "canonical_state" in data:
            data["canonical_state"]["date"] = market_date

        if "date" in data:
            data["date"] = market_date

        return data

    except:
        return None


st.set_page_config(page_title="Bitcoin Organism Observatory", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 0.8rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🧬 BITCOIN ORGANISM OBSERVATORY")

data = {k: load_json(v) for k, v in FILES.items()}

observatory = data["observatory"]
pulse = data["pulse"]
brain = data["brain"]
sync = data["sync"]
cycle = data["cycle"]


# ================================
# EVOLUTION RADAR
# ================================

st.subheader("Evolution Radar")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if observatory:
        radar_box("Evolution Stage", observatory.get("evolution_stage"))

with col2:
    if pulse:
        radar_box("Pulse State", pulse.get("pulse_state"))

with col3:
    if brain:
        radar_box("Model State", brain.get("model_state"))

with col4:
    if cycle:
        radar_box("Cycle Phase", cycle.get("cycle_signal"))


# ================================
# EVOLUTION MOMENTUM
# ================================

st.subheader("Evolution Momentum")

try:

    df = pd.read_csv(PRESSURE_FILE)
    df = df.sort_values("month")

    if len(df) >= 2:

        momentum = df.iloc[-1]["pressure"] - df.iloc[-2]["pressure"]

        colM1, colM2 = st.columns(2)

        colM1.metric("Momentum", round(momentum,3))

        if momentum > 0:
            colM2.success("Expansion energy increasing")

        elif momentum < 0:
            colM2.warning("Compression building")

        else:
            colM2.info("System stable")

except:

    st.write("Momentum unavailable")


# ================================
# EVOLUTION PRESSURE TIMELINE
# ================================

st.subheader("Evolution Pressure Timeline")

try:

    df = pd.read_csv(PRESSURE_FILE)

    df["date"] = (
        df["month"]
        .str.replace("bitcoin_", "", regex=False)
        .str.replace("_", "-")
    )

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m", errors="coerce")

    df = df.dropna(subset=["date"])
    df = df.sort_values("date")

    fig, ax = plt.subplots(figsize=(12,4))

    ax.plot(
        df["date"],
        df["pressure"],
        linewidth=2,
        color="black"
    )

    # bandas de regime
    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.3)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.3)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.3)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.3)

    # mostrar todo o histórico
    ax.set_ylim(0,7)

    import matplotlib.dates as mdates

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.set_xlabel("Year")
    ax.set_ylabel("Pressure")
    ax.set_title("Evolution Pressure Timeline")

    fig.autofmt_xdate()

    st.pyplot(fig)

    if len(df) >= 2:

        last_two = df.tail(2)

        colA, colB = st.columns(2)

        colA.metric(
            last_two.iloc[0]["date"].strftime("%Y-%m"),
            round(last_two.iloc[0]["pressure"],3)
        )

        colB.metric(
            last_two.iloc[1]["date"].strftime("%Y-%m"),
            round(last_two.iloc[1]["pressure"],3)
        )

except Exception as e:

    st.error("Pressure timeline error")
    st.write(e)


# ================================
# REGIME + MACRO
# ================================

cols = st.columns(2)

with cols[0]:

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


with cols[1]:

    st.subheader("Macro Synchronization")

    if sync:

        sync_state = sync.get("synchronization_state")

        if sync_state == "aligned":
            st.success("Global synchronization detected")

        elif sync_state == "neutral":
            st.info("Global systems neutral")

        else:
            st.warning("Macro misalignment detected")
# ================================
# DYNAMIC EVOLUTION FIELD
# ================================

st.subheader("Dynamic Evolution Field")

try:

    df = pd.read_csv(PRESSURE_FILE)

    fig, ax = plt.subplots(figsize=(9,4))

    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.35)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.35)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.35)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.35)

    ax.scatter(df["tension"], df["pressure"], s=25, alpha=0.4)

    recent = df.tail(6)

    ax.plot(recent["tension"], recent["pressure"], linewidth=2)

    if len(df) >= 2:

        current = df.iloc[-1]
        prev = df.iloc[-2]

        ax.scatter(current["tension"], current["pressure"], s=200)

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

        st.success(
            f"Current Position → Tension {round(current['tension'],3)} | Pressure {round(current['pressure'],3)}"
        )

    ax.set_xlabel("Tension")
    ax.set_ylabel("Pressure")
    ax.set_title("Market Evolution Phase Space")

    st.pyplot(fig)

except:

    st.write("Phase map data not available")


# ================================
# NEXT EVOLUTION VECTOR
# ================================

st.subheader("Next Evolution Vector")

try:

    if len(df) >= 2:

        delta_pressure = df.iloc[-1]["pressure"] - df.iloc[-2]["pressure"]
        delta_tension = df.iloc[-1]["tension"] - df.iloc[-2]["tension"]

        if delta_pressure > 0 and delta_tension > 0:
            st.success("↗ Expansion building")

        elif delta_pressure < 0 and delta_tension < 0:
            st.warning("↘ Compression forming")

        else:
            st.info("→ Transitional state")

except:

    st.write("Vector unavailable")


# ================================
# ORGANISM HEARTBEAT
# ================================

st.subheader("Organism Heartbeat")

heartbeat = get_latest_heartbeat()

if heartbeat:

    st.success("Heartbeat detected")
    st.json(heartbeat)

else:

    st.write("Heartbeat not detected")


# ================================
# MISSION CONTROL
# ================================

st.subheader("Organism Mission Control")

colA, colB, colC = st.columns(3)

with colA:

    st.write("Organism Engine ● READY")

    if st.button("Run Full Organism"):
        os.system("./run_bitcoin_organism.sh")
        st.success("Organism cycle executed")

with colB:

    st.write("Physiology Engine ● READY")

    if st.button("Run Physiology Engine"):
        os.system("python -m engine.physiology_generator_engine")
        st.success("Physiology updated")

with colC:

    st.write("Evolution Engine ● READY")

    if st.button("Run Evolution Engine"):
        os.system("python -m engine.evolution_pressure_engine")
        st.success("Evolution recalculated")


# ================================
# SYSTEM DATA
# ================================

st.subheader("System Data")

st.json({
    "observatory": observatory,
    "pulse": pulse,
    "brain": brain,
    "cycle": cycle
})
