import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


print(“PHASE MAP MODULE LOADED”)


def render_phase_map(df):

    st.subheader("Evolution Phase Space")

    if df is None or df.empty:
        st.write("Phase space data unavailable")
        return

    fig, ax = plt.subplots(figsize=(7,5))

    # zonas de regime
    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.35)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.35)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.35)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.35)

    # histórico completo
    ax.scatter(df["tension"], df["pressure"], s=15, alpha=0.3)

    # últimos pontos
    recent = df.tail(6)

    ax.plot(recent["tension"], recent["pressure"], linewidth=2)

    # posição atual
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

    ax.set_xlabel("Tension")
    ax.set_ylabel("Pressure")
    ax.set_title("Market Evolution Phase Space")

    st.pyplot(fig)

    st.success(
        f"Current Position → Tension {round(current['tension'],3)} | Pressure {round(current['pressure'],3)}"
    )
