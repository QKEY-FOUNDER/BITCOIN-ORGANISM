import streamlit as st

from dashboard.modules.loader import load_system_state, load_pressure
from dashboard.modules.radar import render_radar
from dashboard.modules.timeline import render_timeline


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
# FOOTER
# ================================

st.markdown("---")

st.caption("Bitcoin Organism Observatory — Evolution Monitoring System")
