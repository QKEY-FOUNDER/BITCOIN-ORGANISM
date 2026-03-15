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

    # velocidade da animação
    speed = st.slider("Animation speed (seconds per frame)", 0.05, 1.0, 0.25)

    tension = df["tension"].values
    pressure = df["pressure"].values

    xy = np.vstack([tension, pressure])
    kde = gaussian_kde(xy)

    xmin, xmax = 0, tension.max() + 0.05
    ymin = max(0, pressure.min() - 0.25)
    ymax = pressure.max() + 0.35

    xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
    grid = np.vstack([xx.ravel(), yy.ravel()])
    density = kde(grid).reshape(xx.shape)

    colors = [
        "#0050ff",   # passado distante
        "#4a6cff",   # passado recente
        "#9b4dff",   # epicentro
        "#ff6b6b",   # futuro próximo
        "#ff0000"    # futuro distante
    ]

    sizes = [
        260,
        180,
        120,
        70,
        35
    ]

    placeholder = st.empty()

    for i in range(len(df)):

        fig, ax = plt.subplots(figsize=(10,3))

        # bandas de regime
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

        # janela deslizante de 5 meses
        idx = [
            max(i-2,0),
            max(i-1,0),
            i,
            min(i+1,len(df)-1),
            min(i+2,len(df)-1)
        ]

        for j, k in enumerate(idx):

            p = df.iloc[k]

            # pequeno efeito pulsante no epicentro
            size = sizes[j]
            if j == 2:
                size = size + math.sin(i * 0.4) * 20

            ax.scatter(
                p["tension"],
                p["pressure"],
                s=size,
                color=colors[j],
                alpha=0.95,
                zorder=3
            )

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        ax.set_xlabel("Tension")
        ax.set_ylabel("Pressure")

        ax.set_title("Bitcoin Organism Evolution")

        plt.tight_layout()

        placeholder.pyplot(fig)

        time.sleep(speed)
