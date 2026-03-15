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

    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.35)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.35)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.35)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.35)

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

    # campo suave
    ax.contourf(
        xx,
        yy,
        density,
        levels=8,
        alpha=0.16
    )

    # contornos
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

    # ================================
    # CURRENT POSITION
    # ================================

    current = df.iloc[-1]
    prev = df.iloc[-2]

    ax.scatter(
        current["tension"],
        current["pressure"],
        s=140,
        color="#ff7f0e",
        zorder=4
    )

    # vetor histórico imediato
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
    # PROBABLE TRAJECTORY (KDE GRADIENT)
    # ================================

    # encontrar célula mais próxima
    ix = np.abs(xx[:,0] - current["tension"]).argmin()
    iy = np.abs(yy[0,:] - current["pressure"]).argmin()

    # gradiente do campo
    gy, gx = np.gradient(density)

    grad_x = gx[ix, iy]
    grad_y = gy[ix, iy]

    scale = 0.15

    ax.arrow(
        current["tension"],
        current["pressure"],
        grad_x * scale,
        grad_y * scale,
        head_width=0.015,
        color="red",
        linewidth=2
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
