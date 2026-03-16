import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import time
import math


def render_galaxy_animation(df):

    st.subheader("Bitcoin Evolution Galaxy")

    if df is None or df.empty:
        st.write("Galaxy animation unavailable")
        return

    speed = st.slider("Animation speed (seconds per frame)", 0.02, 0.5, 0.08)

    tension = df["tension"].values
    pressure = df["pressure"].values

    # =========================
    # KDE FIELD (fundo Phase Space)
    # =========================

    xy = np.vstack([tension, pressure])
    kde = gaussian_kde(xy)

    xmin, xmax = 0, tension.max() + 0.05
    ymin = max(0, pressure.min() - 0.25)
    ymax = pressure.max() + 0.35

    xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    grid = np.vstack([xx.ravel(), yy.ravel()])
    density = kde(grid).reshape(xx.shape)

    placeholder = st.empty()

    angle = 0

    for i in range(1, len(df)):

        fig, ax = plt.subplots(figsize=(10,3))

        # bandas iguais ao Phase Space
        ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.22)
        ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.22)
        ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.22)
        ax.axhspan(3.8,10,color="#fecaca",alpha=0.22)

        # campo de densidade
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

        # =========================
        # PONTO ATUAL (epicentro)
        # =========================

        current = df.iloc[i]
        prev = df.iloc[i-1]

        cx = current["tension"]
        cy = current["pressure"]

        # vetor movimento
        dx = cx - prev["tension"]
        dy = cy - prev["pressure"]

        norm = math.sqrt(dx*dx + dy*dy) + 1e-6

        dx /= norm
        dy /= norm

        # vetor perpendicular
        px = -dy
        py = dx

        # rotação orbital
        angle += math.radians(30)

        r1 = 0.04
        r2 = 0.08

        rotx = math.cos(angle)
        roty = math.sin(angle)

        # caudas azuis (passado)
        tail1x = cx + r1*(px*rotx - dx*roty)
        tail1y = cy + r1*(py*rotx - dy*roty)

        tail2x = cx + r2*(px*rotx - dx*roty)
        tail2y = cy + r2*(py*rotx - dy*roty)

        # caudas vermelhas (futuro)
        head1x = cx - r1*(px*rotx - dx*roty)
        head1y = cy - r1*(py*rotx - dy*roty)

        head2x = cx - r2*(px*rotx - dx*roty)
        head2y = cy - r2*(py*rotx - dy*roty)

        # =========================
        # DESENHAR GALÁXIA
        # =========================

        ax.scatter(cx, cy, s=160, color="#9b4dff", zorder=5)     # epicentro

        ax.scatter(tail1x, tail1y, s=110, color="#4a6cff")
        ax.scatter(tail2x, tail2y, s=200, color="#0050ff")

        ax.scatter(head1x, head1y, s=70, color="#ff6b6b")
        ax.scatter(head2x, head2y, s=40, color="#ff0000")

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        ax.set_xlabel("Tension")
        ax.set_ylabel("Pressure")

        ax.set_title("Bitcoin Organism Evolution")

        plt.tight_layout()

        placeholder.pyplot(fig)

        time.sleep(speed)
