import streamlit as st
import matplotlib.pyplot as plt


def render_phase_map(df):

    st.subheader("Evolution Phase Space")

    if df is None or df.empty:
        st.write("Phase space data unavailable")
        return

    fig, ax = plt.subplots(figsize=(10,1.9))

    # bandas de regime
    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.35)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.35)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.35)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.35)

    # histórico
    ax.scatter(df["tension"], df["pressure"], s=7, alpha=0.20)

    # trajetória recente
    recent = df.tail(6)
    ax.plot(recent["tension"], recent["pressure"], linewidth=2)

    current = df.iloc[-1]
    prev = df.iloc[-2]

    # posição atual
    ax.scatter(current["tension"], current["pressure"], s=110, zorder=3)

    dx = current["tension"] - prev["tension"]
    dy = current["pressure"] - prev["pressure"]

    # vetor de movimento
    ax.arrow(
        prev["tension"],
        prev["pressure"],
        dx,
        dy,
        head_width=0.012,
        length_includes_head=True,
        linewidth=2
    )

    ax.set_xlabel("Tension")
    ax.set_ylabel("Pressure")

    # limites compactos
    ymin = max(0, df["pressure"].min() - 0.25)
    ymax = df["pressure"].max() + 0.35
    ax.set_ylim(ymin, ymax)

    # remover espaço morto
    plt.tight_layout(pad=0.1)

    st.pyplot(fig)

    st.success(
        f"Current Position → Tension {round(current['tension'],3)} | Pressure {round(current['pressure'],3)}"
    )
