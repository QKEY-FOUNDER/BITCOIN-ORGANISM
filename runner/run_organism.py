import os
import subprocess

# Root of the project
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENGINE_PATH = os.path.join(BASE_PATH, "engine", "core_engine.py")
DATA_PATH = os.path.join(BASE_PATH, "data")
OUTPUT_PATH = os.path.join(BASE_PATH, "output")

os.makedirs(OUTPUT_PATH, exist_ok=True)

def run_month(csv_file):
    print("🧬 Processing:", csv_file)

    env = os.environ.copy()
    env["CSV_PATH"] = csv_file

    subprocess.run(
        ["python", ENGINE_PATH],
        env=env,
        cwd=BASE_PATH
    )

def walk_data_tree():
    for root, dirs, files in os.walk(DATA_PATH):
        for f in sorted(files):
            if f.endswith(".csv"):
                yield os.path.join(root, f)

if __name__ == "__main__":
    print("🌍 Bitcoin Organism Awakening")

    for csv_file in walk_data_tree():
        run_month(csv_file)

    print("✨ Evolution complete. The organism has spoken.")
