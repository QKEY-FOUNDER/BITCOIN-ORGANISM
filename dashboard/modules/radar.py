import streamlit as st


def radar_box(title, value):

    st.markdown(f"""
    <div style="background:#f7f7f7;padding:10px;border-radius:8px">
        <div style="font-size:12px;color:#666">{title}</div>
        <div style="font-size:18px;font-weight:600">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_radar(state):

    st.subheader("Evolution Radar")

    col1, col2, col3, col4 = st.columns(4)

    observatory = state.get("observatory")
    pulse = state.get("pulse")
    brain = state.get("brain")
    cycle = state.get("cycle")

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
