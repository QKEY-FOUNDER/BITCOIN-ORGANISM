import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import time


# ================================
# COMET TRAIL (DYNAMIC ENERGY)
# ================================

def draw_comet_trail(ax, x_prev2, y_prev2, x_prev1, y_prev1, x, y, accel):

    dx = x - x_prev1
    dy = y - y_prev1

    dist = np.sqrt(dx**2 + dy**2)
    if dist == 0:
        return

    perp_x = -dy / dist
    perp_y = dx / dist

    curvature = 0.05 + accel * 1.0
    vertical_scale = 0.1 + accel * 1.5

    steps = 30
    t = np.linspace(0, 1, steps)

    curve_x = x_prev1 + dx * t + perp_x * curvature * np.sin(np.pi * t)
    curve_y = y_prev1 + dy * t + perp_y * vertical_scale * np.sin(np.pi * t)

    for i in range(len(t) - 1):

        fade = i / len(t)

        alpha = 0.2 + 0.8 * fade + accel
        alpha = min(alpha, 1)

        width = 1.2 + accel * 4

        ax.plot(
            curve_x[i:i+2],
            curve_y[i:i+2],
            color=(0.2, 0.7, 1.0, alpha),
            linewidth=width
        )


# ================================
# MAIN RENDER
# ================================

def render_galaxy_phase_animation(df):

    st.subheader("Bitcoin Evolution Galaxy")

    if df is None or df.empty or len(df) < 3:
        st.warning("Not enough data")
        return

    speed = st.slider("Base speed", 0.01, 0.5, 0.06)

    tension = df["tension"].values
    pressure = df["pressure"].values

    placeholder = st.empty()

    # energia global (para respiração)
    global_energy = np.std(pressure)

    for i in range(2, len(df)):

        fig, ax = plt.subplots(figsize=(10, 3))

        # ================================
        # DATA
        # ================================

        prev2 = df.iloc[i-2]
        prev1 = df.iloc[i-1]
        current = df.iloc[i]

        x = current["tension"]
        y = current["pressure"]

        # ================================
        # ENERGY (MASTER VARIABLE)
        # ================================

        v1x = prev1["tension"] - prev2["tension"]
        v1y = prev1["pressure"] - prev2["pressure"]

        v2x = current["tension"] - prev1["tension"]
        v2y = current["pressure"] - prev1["pressure"]

        accel = np.sqrt((v2x - v1x)**2 + (v2y - v1y)**2)
        accel = min(accel, 0.2)

        # ================================
        # BREATHING SPACE (NOVO)
        # ================================

        breath = 1 + 0.05 * np.sin(i * 0.15) + global_energy * 0.05

        xmin, xmax = 0, max(tension) + 0.05
        ymin = max(0, min(pressure) - 0.25)
        ymax = max(pressure) + 0.35

        x_center = (xmin + xmax) / 2
        y_center = (ymin + ymax) / 2

        x_range = (xmax - xmin) * breath
        y_range = (ymax - ymin) * breath

        xmin_b = x_center - x_range / 2
        xmax_b = x_center + x_range / 2
        ymin_b = y_center - y_range / 2
        ymax_b = y_center + y_range / 2

        # ================================
        # BACKGROUND
        # ================================

        ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.18)
        ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.18)
        ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.18)
        ax.axhspan(3.8,10,color="#fecaca",alpha=0.18)

        xy = np.vstack([tension, pressure])
        kde = gaussian_kde(xy)

        xx, yy = np.mgrid[xmin_b:xmax_b:200j, ymin_b:ymax_b:200j]
        grid = np.vstack([xx.ravel(), yy.ravel()])
        density = kde(grid).reshape(xx.shape)

        ax.contourf(xx, yy, density, levels=8, alpha=0.10)

        # ================================
        # COMET TRAIL
        # ================================

        draw_comet_trail(
            ax,
            prev2["tension"],
            prev2["pressure"],
            prev1["tension"],
            prev1["pressure"],
            current["tension"],
            current["pressure"],
            accel
        )

        # ================================
        # ORBITAL MOTION
        # ================================

        angle = i * (0.2 + accel * 2)

        r1 = 0.02 + accel * 0.03
        r2 = 0.04 + accel * 0.05

        size_base = 80 + accel * 200

        ax.scatter(
            x + r2 * np.cos(angle),
            y + r2 * np.sin(angle),
            s=size_base,
            color=(0.2, 0.4, 1.0, 0.9)
        )

        ax.scatter(
            x + r1 * np.cos(angle + np.pi),
            y + r1 * np.sin(angle + np.pi),
            s=size_base * 0.6,
            color=(0.3, 0.5, 1.0, 0.7)
        )

        ax.scatter(
            x + r2 * np.cos(angle + np.pi/2),
            y + r2 * np.sin(angle + np.pi/2),
            s=size_base * 0.6,
            color=(1.0, 0.3, 0.3, 0.8)
        )

        ax.scatter(
            x + r1 * np.cos(angle - np.pi/2),
            y + r1 * np.sin(angle - np.pi/2),
            s=size_base * 0.4,
            color=(1.0, 0.4, 0.4, 0.6)
        )

        # ================================
        # EPICENTER
        # ================================

        epicenter_size = 120 + accel * 300

        ax.scatter(
            x,
            y,
            s=epicenter_size,
            color=(0.6, 0.0, 0.8, 1.0),
            zorder=5
        )

        # ================================
        # TIME FLOW
        # ================================

        dynamic_speed = speed * (1.2 - accel * 5)
        dynamic_speed = max(0.01, min(dynamic_speed, 0.3))

        # ================================
        # AXIS
        # ================================

        ax.set_xlim(xmin_b, xmax_b)
        ax.set_ylim(ymin_b, ymax_b)

        ax.set_xlabel("Tension")
        ax.set_ylabel("Pressure")

        ax.set_title("Bitcoin Organism Evolution")

        plt.tight_layout()

        placeholder.pyplot(fig)

        time.sleep(dynamic_speed)
