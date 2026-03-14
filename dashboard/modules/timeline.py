import streamlit as st
import matplotlib.pyplot as plt


def render_timeline(df):

    st.subheader("Evolution Pressure Timeline")

    if df is None or df.empty:
        st.write("Pressure data not available")
        return

    fig, ax = plt.subplots(figsize=(12,3))

    ax.plot(df["date"], df["pressure"], linewidth=2)

    # bandas evolutivas do sistema
    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.3)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.3)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.3)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.3)

    ax.set_xlabel("Year")
    ax.set_ylabel("Pressure")
    ax.set_title("Evolution Pressure Timeline")

    fig.autofmt_xdate()

    st.pyplot(fig)

    last_two = df.tail(2)

    colA, colB = st.columns(2)

    colA.metric(
        last_two.iloc[0]["date"].strftime("%Y-%m"),
        round(last_two.iloc[0]["pressure"],3)
    )

    colB.metric(
        last_two.iloc[1]["date"].strftime("%Y-%m"),
        round(last_two.iloc[1]["pressure"],3)
    )
