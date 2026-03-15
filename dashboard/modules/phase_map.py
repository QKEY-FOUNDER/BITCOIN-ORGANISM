import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


def render_phase_map(df):

    st.subheader("Evolution Phase Space")

    if df is None or df.empty:
        st.write("Phase space data unavailable")
        return

    tension = df["tension"].values
    pressure = df["pressure"].values

    fig, ax = plt.subplots(figsize=(10,2))

    # ================================
    # REGIME BANDS
    # ================================

    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.22)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.22)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.22)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.22)

    # ================================
    # KDE FIELD
    # ================================

    xy = np.vstack([tension, pressure])
    kde = gaussian_kde(xy)

    xmin, xmax = 0, tension.max() + 0.05
    ymin = max(0, pressure.min() - 0.25)
    ymax = pressure.max() + 0.35

    xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    grid = np.vstack([xx.ravel(), yy.ravel()])
    density = kde(grid).reshape(xx.shape)

    ax.contourf(
        xx,
        yy,
        density,
        levels=8,
        alpha=0.16
    )

    ax.contour(
        xx,
        yy,
        density,
        levels=5,
        linewidths=0.4,
        alpha=0.25
    )

    # ================================
    # HISTORICAL POINTS
    # ================================

    ax.scatter(
        tension,
        pressure,
        s=6,
        alpha=0.18
    )

    # ================================
    # RECENT TRAJECTORY
    # ================================

    recent = df.tail(12)

    ax.plot(
        recent["tension"],
        recent["pressure"],
        linewidth=2.2,
        color="#1f77b4"
    )

    current = df.iloc[-1]
    prev = df.iloc[-2]

    ax.scatter(
        current["tension"],
        current["pressure"],
        s=140,
        color="#ff7f0e",
        zorder=4
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
    # FIND ATTRACTOR CENTER
    # ================================

    max_density_idx = np.unravel_index(np.argmax(density), density.shape)

    attractor_x = xx[max_density_idx]
    attractor_y = yy[max_density_idx]

    ax.scatter(
        attractor_x,
        attractor_y,
        s=60,
        color="black",
        zorder=5
    )

    # ================================
    # DISTANCE TO ATTRACTOR
    # ================================

    dist = np.sqrt(
        (current["tension"] - attractor_x)**2 +
        (current["pressure"] - attractor_y)**2
    )

    # ================================
    # AXIS
    # ================================

    ax.set_xlabel("Tension")
    ax.set_ylabel("Pressure")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    plt.tight_layout(pad=0.1)

    st.pyplot(fig)

    st.success(
        f"Current Position → Tension {round(current['tension'],3)} | Pressure {round(current['pressure'],3)}"
    )

    # ================================
    # SYSTEM STATE
    # ================================

    if dist < 0.15:
        status = "Near equilibrium"
    elif dist < 0.35:
        status = "Moderate displacement"
    else:
        status = "High disequilibrium"

    st.info(
        f"Distance to Attractor → {round(dist,3)} | System Status → {status}"
    )
