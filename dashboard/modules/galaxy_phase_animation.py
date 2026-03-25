import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import time

def draw_comet_trail(ax, x_prev2, y_prev2, x_prev1, y_prev1, x, y, accel):
    dx = x - x_prev1
    dy = y - y_prev1
    dist = np.sqrt(dx**2 + dy**2)
    if dist == 0:
        return
    perp_x = -dy / dist
    perp_y = dx / dist
    t = np.linspace(0, 1, 30)
    curve_x = x_prev1 + dx * t + perp_x * (0.05 + accel) * np.sin(np.pi * t)
    curve_y = y_prev1 + dy * t + perp_y * (0.1 + accel) * np.sin(np.pi * t)
    for i in range(len(t) - 1):
        alpha = min(0.3 + accel, 1)
        ax.plot(curve_x[i:i+2], curve_y[i:i+2], color=(0.2,0.7,1,alpha), linewidth=1.5)

def draw_ghost_field(ax, history, xmin, xmax, ymin, ymax):
    if len(history) < 3:
        return
    points = np.array(history)
    if np.linalg.matrix_rank(points - points.mean(axis=0)) < 2:
        return
    try:
        kde = gaussian_kde(points.T)
        xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        grid = np.vstack([xx.ravel(), yy.ravel()])
        density = kde(grid).reshape(xx.shape)
        ax.contourf(xx, yy, density, levels=6, cmap="Blues", alpha=0.1)
    except:
        return

def compute_gravity_center(history):
    if len(history) < 3:
        return None
    pts = np.array(history)
    weights = np.linspace(0.5, 1.5, len(pts))
    weights /= weights.sum()
    return np.sum(pts * weights[:, None], axis=0)

def project_future_path(history):
    if len(history) < 3:
        return []
    pts = np.array(history)
    vel = np.diff(pts, axis=0).mean(axis=0)
    future = []
    cur = pts[-1].copy()
    for i in range(6):
        cur = cur + vel * (0.9 ** i)
        future.append(cur.copy())
    return np.array(future)

def render_galaxy_phase_animation(df):

    st.subheader("Bitcoin Evolution Galaxy")

    if df is None or df.empty or len(df) < 3:
        st.warning("Not enough data")
        return

    speed = st.slider("Base speed", 0.01, 0.25, 0.04)

    tension = df["tension"].values
    pressure = df["pressure"].values

    xmin, xmax = 0, max(tension) + 0.05
    ymin = max(0, min(pressure) - 0.25)
    ymax = max(pressure) + 0.35

    placeholder = st.empty()

    history = []
    prev_angle = 0

    for i in range(2, len(df)):

        fig, ax = plt.subplots(figsize=(10, 3))

        p2 = df.iloc[i-2]
        p1 = df.iloc[i-1]
        cur = df.iloc[i]

        x = cur["tension"]
        y = cur["pressure"]

        accel = min(np.linalg.norm([
            (cur["tension"] - p1["tension"]) - (p1["tension"] - p2["tension"]),
            (cur["pressure"] - p1["pressure"]) - (p1["pressure"] - p2["pressure"])
        ]), 0.2)

        center = compute_gravity_center(history)
        if center is not None:
            dx, dy = center - np.array([x, y])
            dist = np.linalg.norm([dx, dy]) + 1e-5
            x += dx/dist * 0.01
            y += dy/dist * 0.01
            ax.scatter(center[0], center[1], s=120, color="yellow")

        ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.15)
        ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.15)
        ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.15)
        ax.axhspan(3.8,10,color="#fecaca",alpha=0.15)

        xy = np.vstack([tension, pressure])
        kde = gaussian_kde(xy)
        xx, yy = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
        grid = np.vstack([xx.ravel(), yy.ravel()])
        density = kde(grid).reshape(xx.shape)
        ax.contourf(xx, yy, density, alpha=0.05)

        draw_ghost_field(ax, history, xmin, xmax, ymin, ymax)

        draw_comet_trail(ax,
            p2["tension"], p2["pressure"],
            p1["tension"], p1["pressure"],
            x, y, accel
        )

        angle = prev_angle + 0.1
        prev_angle = angle

        ax.scatter(x + 0.03*np.cos(angle), y + 0.03*np.sin(angle), s=80, color="blue")
        ax.scatter(x, y, s=100, color="purple")

        future = project_future_path(history)
        if len(future) > 0:
            ax.plot(future[:,0], future[:,1], linestyle="dashed")

        history.append((x, y))
        if len(history) > 5:
            history.pop(0)

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        ax.set_xlabel("Tension")
        ax.set_ylabel("Pressure")

        placeholder.pyplot(fig)

        time.sleep(max(0.02, speed * (1 - accel)))
