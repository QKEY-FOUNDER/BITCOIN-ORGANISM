import csv
import os
from datetime import datetime

DOM_FILE = "btc_dominance_daily_gecko.csv"

# ─────────────────────────────────────────────
# Carregar dominância diária para memória
# ─────────────────────────────────────────────
dominance = {}

with open(DOM_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dominance[row["date"]] = row["btc_dominance"]

# ─────────────────────────────────────────────
# Processar todos os ficheiros mensais
# ─────────────────────────────────────────────
for fname in sorted(os.listdir(".")):
    if not fname.startswith("bitcoin_") or not fname.endswith(".csv"):
        continue

    print(f"🔄 merging {fname}")

    rows = []
    with open(fname, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        if "DominanceBTC" in fieldnames:
            print(f"  ⚠️  já contém DominanceBTC — ignorado")
            continue

        for row in reader:
            date = row["Date"]
            row["DominanceBTC"] = dominance.get(date, "")
            rows.append(row)

    new_fields = fieldnames + ["DominanceBTC"]

    with open(fname, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  ✅ merged {fname}")

print("\n🏁 Fusão concluída com sucesso.")
