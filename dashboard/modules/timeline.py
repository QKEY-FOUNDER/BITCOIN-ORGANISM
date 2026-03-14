import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


# eventos históricos do organismo
BITCOIN_EVENTS = {
    "2010-07-01": "Early Network Growth",
    "2013-04-01": "First Major Bubble",
    "2014-02-01": "MtGox Collapse",
    "2016-07-01": "Second Halving",
    "2017-12-01": "2017 Mania Peak",
    "2020-05-01": "Third Halving",
    "2021-11-01": "Institutional Peak",
    "2024-04-01": "Fourth Halving",
}


def render_timeline(df):

    st.subheader("Evolution Pressure Timeline")

    if df is None or df.empty:
        st.write("Pressure data not available")
        return

    fig, ax = plt.subplots(figsize=(12,3))

    ax.plot(df["date"], df["pressure"], linewidth=2)

    # bandas evolutivas
    ax.axhspan(0,1.2,color="#c7d2fe",alpha=0.3)
    ax.axhspan(1.2,2.5,color="#bbf7d0",alpha=0.3)
    ax.axhspan(2.5,3.8,color="#fde68a",alpha=0.3)
    ax.axhspan(3.8,10,color="#fecaca",alpha=0.3)

    # desenhar eventos históricos
    for date_str, label in BITCOIN_EVENTS.items():

        event_date = pd.to_datetime(date_str)

        ax.axvline(event_date, linestyle="dashed", linewidth=1)

        ax.text(
            event_date,
            ax.get_ylim()[1]*0.95,
            label,
            rotation=90,
            fontsize=8,
            verticalalignment="top"
        )

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
