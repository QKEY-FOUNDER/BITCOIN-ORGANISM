from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PHASE_METRICS_FILE = PROJECT_ROOT / "data" / "phase_metrics.csv"
CURRENT_DATA_FILE = PROJECT_ROOT / "data" / "market" / "final" / "btc_daily_full.csv"


def compute_current_metrics(df, window=90):
    df = df.sort_values("Date").tail(window).copy()
    df["Return"] = df["Close"].pct_change()

    returns = df["Return"].dropna()

    if len(returns) == 0:
        return None

    cumulative_return = float((df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1)
    volatility = float(returns.std())
    max_drawdown = float(((df["Close"] / df["Close"].cummax()) - 1).min())

    return np.array([cumulative_return, volatility, max_drawdown], dtype=float)


def normalize_vector(v):
    v = np.array(v, dtype=float)
    return (v - np.mean(v)) / (np.std(v) + 1e-8)


def get_phase_similarity():
    if not PHASE_METRICS_FILE.exists():
        return None

    if not CURRENT_DATA_FILE.exists():
        return None

    phase_df = pd.read_csv(PHASE_METRICS_FILE)
    current_df = pd.read_csv(CURRENT_DATA_FILE, parse_dates=["Date"])

    current_vector = compute_current_metrics(current_df)

    if current_vector is None:
        return None

    similarities = []

    for _, row in phase_df.iterrows():

        phase_vector = np.array([
            float(row["cumulative_return"]),
            float(row["volatility"]),
            float(row["max_drawdown"])
        ], dtype=float)

        distance = np.linalg.norm(
            normalize_vector(current_vector) -
            normalize_vector(phase_vector)
        )

        similarities.append({
            "phase": row["phase"],
            "distance": float(round(distance, 4))
        })

    sim_df = pd.DataFrame(similarities).sort_values("distance")

    if sim_df.empty:
        return None

    best_match = sim_df.iloc[0]

    return {
        "historical_similarity_phase": str(best_match["phase"]),
        "historical_similarity_distance": float(best_match["distance"])
    }


if __name__ == "__main__":
    result = get_phase_similarity()
    if result:
        print(result)
    else:
        print("Sem dados suficientes")
