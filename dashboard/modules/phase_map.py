import streamlit as st
import matplotlib.pyplot as plt


def render_phase_map(df):

    st.subheader("Evolution Phase Space")

    if df is None or df.empty:
        st.write("Phase space data unavailable")
        return

    tension = df["tension"]
    pressure = df["pressure"]

    fig, ax = plt.subplots(figsize=(10,2))

    # ================================
    # REGIME BANDS
    # ================================

    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.35)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.35)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.35)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.35)

    # ================================
    # ATTRACTOR DENSITY (HEXBIN)
    # ================================

    ax.hexbin(
        tension,
        pressure,
        gridsize=30,
        mincnt=1,
        alpha=0.25
    )

    # ================================
    # HISTORICAL POINTS
    # ================================

    ax.scatter(
        tension,
        pressure,
        s=6,
        alpha=0.15
    )

    # ================================
    # RECENT TRAJECTORY
    # ================================

    recent = df.tail(12)

    ax.plot(
        recent["tension"],
        recent["pressure"],
        linewidth=2
    )

    # ================================
    # CURRENT POSITION
    # ================================

    current = df.iloc[-1]
    prev = df.iloc[-2]

    ax.scatter(
        current["tension"],
        current["pressure"],
        s=120,
        zorder=3
    )

    dx = current["tension"] - prev["tension"]
    dy = current["pressure"] - prev["pressure"]

    ax.arrow(
        prev["tension"],
        prev["pressure"],
        dx,
        dy,
        head_width=0.012,
        length_includes_head=True,
        linewidth=2
    )

    # ================================
    # AXIS
    # ================================

    ax.set_xlabel("Tension")
    ax.set_ylabel("Pressure")

    ymin = max(0, pressure.min() - 0.25)
    ymax = pressure.max() + 0.35

    ax.set_ylim(ymin, ymax)
    ax.set_xlim(0, tension.max() + 0.05)

    plt.tight_layout(pad=0.1)

    st.pyplot(fig)

    st.success(
        f"Current Position → Tension {round(current['tension'],3)} | Pressure {round(current['pressure'],3)}"
    )
