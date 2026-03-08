import csv
import os

DOM_FILE = "btc_dominance_daily_gecko.csv"

# Carregar dominância diária
dominance = {}
with open(DOM_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dominance[row["date"]] = row["btc_dominance"]

def merge_file(filename):
    temp_file = filename + ".tmp"

    with open(filename, newline="") as fin, open(temp_file, "w", newline="") as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames or []

        if "DominanceBTC" not in fieldnames:
            fieldnames.append("DominanceBTC")

        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            date = row.get("Date")
            row["DominanceBTC"] = dominance.get(date, "")
            writer.writerow(row)

    os.replace(temp_file, filename)
    print(f"✔ merged {filename}")

def main():
    for file in sorted(os.listdir(".")):
        if file.startswith("bitcoin_") and file.endswith(".csv"):
            merge_file(file)

if __name__ == "__main__":
    main()
