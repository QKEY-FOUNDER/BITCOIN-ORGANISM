import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time


def render_galaxy_animation(df):

    st.subheader("Bitcoin Evolution Galaxy")

    if df is None or df.empty:
        st.write("Galaxy animation unavailable")
        return

    colors = [
        "#0050ff",   # passado distante
        "#4a6cff",   # passado recente
        "#9b4dff",   # epicentro
        "#ff6b6b",   # futuro próximo
        "#ff0000"    # futuro distante
    ]

    sizes = [
        260,   # maior (passado)
        180,
        120,   # epicentro
        70,
        35     # menor (futuro)
    ]

    placeholder = st.empty()

    for i in range(2, len(df)-2):

        fig, ax = plt.subplots(figsize=(10,4))

        points = [
            df.iloc[i-2],
            df.iloc[i-1],
            df.iloc[i],
            df.iloc[i+1],
            df.iloc[i+2]
        ]

        for j, p in enumerate(points):

            ax.scatter(
                p["tension"],
                p["pressure"],
                s=sizes[j],
                color=colors[j],
                alpha=0.9,
                zorder=3
            )

        trajectory = df.iloc[:i+1]

        ax.plot(
            trajectory["tension"],
            trajectory["pressure"],
            linewidth=1.6,
            color="#4aa3ff",
            alpha=0.6
        )

        ax.set_xlabel("Tension")
        ax.set_ylabel("Pressure")

        ax.set_title("Bitcoin Organism Evolution")

        ax.grid(alpha=0.2)

        plt.tight_layout()

        placeholder.pyplot(fig)

        time.sleep(0.30)
