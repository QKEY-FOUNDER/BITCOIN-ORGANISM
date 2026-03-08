import os
import csv
from collections import defaultdict
from datetime import datetime

INPUT_DIR = "data/raw/ohlcv"
OUTPUT_DIR = "data/07_Reconfiguracao_Global_2022_Plus"

os.makedirs(OUTPUT_DIR, exist_ok=True)

monthly = defaultdict(list)

# -------------------------------------------------------
# Helper: safe float
# -------------------------------------------------------

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# -------------------------------------------------------
# Load daily files (2026 only)
# -------------------------------------------------------

for file in os.listdir(INPUT_DIR):
    if file.endswith(".csv") and "2026" in file:
        path = os.path.join(INPUT_DIR, file)

        with open(path, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:

                if not row.get("Date"):
                    continue

                # Normalizar data (remove hora se existir)
                date_str = row["Date"].split(" ")[0]

                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue

                open_p  = safe_float(row.get("Open"))
                high_p  = safe_float(row.get("High"))
                low_p   = safe_float(row.get("Low"))
                close_p = safe_float(row.get("Close"))
                vol_p   = safe_float(row.get("Volume"))
                dom_p   = safe_float(row.get("DominanceBTC"))

                # Ignorar linhas inválidas
                if None in (open_p, high_p, low_p, close_p, vol_p):
                    continue

                key = f"{date.year}_{str(date.month).zfill(2)}"

                monthly[key].append({
                    "Date": date,
                    "Open": open_p,
                    "High": high_p,
                    "Low": low_p,
                    "Close": close_p,
                    "Volume": vol_p,
                    "DominanceBTC": dom_p
                })

# -------------------------------------------------------
# Aggregate monthly
# -------------------------------------------------------

for month, rows in monthly.items():

    if not rows:
        continue

    rows.sort(key=lambda x: x["Date"])

    open_price  = rows[0]["Open"]
    close_price = rows[-1]["Close"]
    high_price  = max(r["High"] for r in rows)
    low_price   = min(r["Low"] for r in rows)
    total_volume = sum(r["Volume"] for r in rows)

    dominance_values = [
        r["DominanceBTC"]
        for r in rows
        if r["DominanceBTC"] is not None
    ]

    avg_dominance = (
        sum(dominance_values) / len(dominance_values)
        if dominance_values
        else 0.0
    )

    output_path = os.path.join(
        OUTPUT_DIR, f"bitcoin_{month}.csv"
    )

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "DominanceBTC"
        ])

        writer.writerow([
            month,
            open_price,
            high_price,
            low_price,
            close_price,
            total_volume,
            avg_dominance
        ])

    print("Created:", output_path)

print("Monthly aggregation complete.")
