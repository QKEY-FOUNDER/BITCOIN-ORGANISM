import streamlit as st
import sys
from pathlib import Path

# garantir que a raiz do repo está no path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# IMPORTS DOS MODULOS (depois do path estar correto)
from dashboard.modules.loader import load_system_state, load_pressure
from dashboard.modules.radar import render_radar
from dashboard.modules.timeline import render_timeline
from dashboard.modules.phase_map import render_phase_map
from dashboard.modules.galaxy_phase_animation import render_galaxy_animation

st.set_page_config(
    page_title="Bitcoin Organism Observatory",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 0.8rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🧬 BITCOIN ORGANISM OBSERVATORY")


# ================================
# LOAD SYSTEM STATE
# ================================

state = load_system_state()

pressure_df = load_pressure()


# ================================
# EVOLUTION RADAR
# ================================

render_radar(state)


# ================================
# EVOLUTION PRESSURE TIMELINE
# ================================

render_timeline(pressure_df)


# ================================
# EVOLUTION PHASE SPACE
# ================================

render_phase_map(pressure_df)

if st.button("▶ Galaxy Evolution"):
    render_galaxy_animation(pressure_df)

# ================================
# FOOTER
# ================================

st.markdown("---")
st.caption("Bitcoin Organism Observatory — Evolution Monitoring System")
