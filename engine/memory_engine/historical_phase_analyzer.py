from pathlib import Path
import pandas as pd
import numpy as np

print("🧠 HISTORICAL PHASE ANALYZER — Memória Estrutural")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = PROJECT_ROOT / "data" / "phase_metrics.csv"


def load_phase_data(phase_path):
    all_files = sorted(phase_path.glob("bitcoin_*.csv"))
    dfs = []

    for file in all_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception:
            continue

    if not dfs:
        return None

    df = pd.concat(dfs, ignore_index=True)

    if "Close" not in df.columns:
        return None

    df = df.sort_values(by="Date")
    df["Return"] = df["Close"].pct_change()

    return df


def compute_metrics(df):
    returns = df["Return"].dropna()

    if len(returns) == 0:
        return None

    cumulative_return = (df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1
    volatility = returns.std()
    max_drawdown = ((df["Close"] / df["Close"].cummax()) - 1).min()

    return {
        "cumulative_return": round(cumulative_return, 4),
        "volatility": round(volatility, 4),
        "max_drawdown": round(max_drawdown, 4)
    }


def main():
    phase_dirs = sorted([d for d in DATA_DIR.iterdir() if d.is_dir() and d.name.startswith("0")])

    results = []

    for phase in phase_dirs:
        print(f"📂 Processando fase: {phase.name}")
        df = load_phase_data(phase)

        if df is None:
            print("⚠️ Sem dados válidos")
            continue

        metrics = compute_metrics(df)

        if metrics is None:
            print("⚠️ Métricas não calculadas")
            continue

        metrics["phase"] = phase.name
        results.append(metrics)

    if not results:
        print("❌ Nenhuma fase analisada")
        return

    result_df = pd.DataFrame(results)
    result_df.to_csv(OUTPUT_FILE, index=False)

    print("\n✅ Métricas por fase geradas:")
    print(result_df)
    print(f"\n📁 Ficheiro salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
