import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import time
import matplotlib.cm as cm


def render_galaxy_animation(df):

    st.subheader("Bitcoin Evolution Galaxy")

    if df is None or df.empty:
        st.write("Galaxy animation unavailable")
        return

    speed = st.slider("Animation speed (seconds per frame)", 0.02, 0.4, 0.06)

    tension = df["tension"].values
    pressure = df["pressure"].values

    # =========================
    # KDE FIELD (mesmo fundo Phase Space)
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

    # mapa de cores gradiente vermelho -> azul
    cmap = cm.get_cmap("coolwarm")

    for i in range(2, len(df)):

        fig, ax = plt.subplots(figsize=(10,3))

        # bandas iguais ao phase space
        ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.22)
        ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.22)
        ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.22)
        ax.axhspan(3.8,10,color="#fecaca",alpha=0.22)

        ax.contourf(xx,yy,density,levels=8,alpha=0.16)
        ax.contour(xx,yy,density,levels=5,linewidths=0.4,alpha=0.25)

        # =========================
        # DESENHAR RASTO
        # =========================

        for j in range(1, i):

            age = j / i
            color = cmap(1-age)

            ax.plot(
                tension[j-1:j+1],
                pressure[j-1:j+1],
                color=color,
                linewidth=3,
                alpha=0.9
            )

        # =========================
        # EPICENTRO
        # =========================

        current = df.iloc[i]

        ax.scatter(
            current["tension"],
            current["pressure"],
            s=180,
            color="red",
            zorder=5
        )

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        ax.set_xlabel("Tension")
        ax.set_ylabel("Pressure")

        ax.set_title("Bitcoin Organism Evolution")

        plt.tight_layout()

        placeholder.pyplot(fig)

        time.sleep(speed)
