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

    speed = st.slider("Animation speed (seconds per frame)",0.02,0.4,0.06)

    tension = df["tension"].values
    pressure = df["pressure"].values

    # KDE background (igual ao phase space)

    xy = np.vstack([tension,pressure])
    kde = gaussian_kde(xy)

    xmin,xmax = 0,tension.max()+0.05
    ymin = max(0,pressure.min()-0.25)
    ymax = pressure.max()+0.35

    xx,yy = np.mgrid[xmin:xmax:200j,ymin:ymax:200j]
    grid = np.vstack([xx.ravel(),yy.ravel()])
    density = kde(grid).reshape(xx.shape)

    placeholder = st.empty()

    for i in range(2,len(df)):

        fig,ax = plt.subplots(figsize=(10,3))

        # regime bands
        ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.22)
        ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.22)
        ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.22)
        ax.axhspan(3.8,10,color="#fecaca",alpha=0.22)

        ax.contourf(xx,yy,density,levels=8,alpha=0.16)
        ax.contour(xx,yy,density,levels=5,linewidths=0.4,alpha=0.25)

        current = df.iloc[i]
        prev = df.iloc[i-1]

        cx = current["tension"]
        cy = current["pressure"]

        # vetor movimento
        dx = cx-prev["tension"]
        dy = cy-prev["pressure"]

        norm = math.sqrt(dx*dx+dy*dy)+1e-6
        dx/=norm
        dy/=norm

        # vetor perpendicular
        px = -dy
        py = dx

        # raio da elipse
        r_major = 0.05
        r_minor = 0.02

        angle = math.radians(i*30)

        cos = math.cos(angle)
        sin = math.sin(angle)

        # passado
        bx = cx + r_major*(dx*cos) + r_minor*(px*sin)
        by = cy + r_major*(dy*cos) + r_minor*(py*sin)

        # presente
        px0 = cx
        py0 = cy

        # futuro
        fx = cx - r_major*(dx*cos) - r_minor*(px*sin)
        fy = cy - r_major*(dy*cos) - r_minor*(py*sin)

        ax.scatter(bx,by,s=120,color="blue",zorder=4)
        ax.scatter(px0,py0,s=160,color="purple",zorder=5)
        ax.scatter(fx,fy,s=80,color="red",zorder=4)

        ax.set_xlim(xmin,xmax)
        ax.set_ylim(ymin,ymax)

        ax.set_xlabel("Tension")
        ax.set_ylabel("Pressure")

        ax.set_title("Bitcoin Organism Evolution")

        plt.tight_layout()

        placeholder.pyplot(fig)

        time.sleep(speed)
