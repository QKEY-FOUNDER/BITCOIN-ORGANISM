# ============================================================
# Dominance Stream — BTC Daily (Infinite, Rate-Limit Safe)
# Coleta 1 ponto de Dominance BTC por dia (CoinGecko)
# Modo: vivo, silencioso, resiliente
# ============================================================

# --- HARDENING BOOT (executa ANTES de qualquer import sensível) ---
import warnings

try:
    from urllib3.exceptions import NotOpenSSLWarning
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
except Exception:
    pass

warnings.filterwarnings("ignore", message=".*LibreSSL.*", category=Warning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# --- Imports ---
from pathlib import Path
import requests
import pandas as pd
from datetime import datetime, timezone
import time
import sys

# --- Banner -------------------------------------------------
print("🔥 DOMINANCE STREAM — BTC DAILY (INFINITE)")
print("=" * 55)

# ------------------------------------------------------------
# ROOTS
# ------------------------------------------------------------
BASE_PATH = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_PATH / "data/raw/dominance"
RAW_DIR.mkdir(parents=True, exist_ok=True)

NORMALIZED_FILE = BASE_PATH / "data/normalized/dominance_daily.csv"

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def today_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_existing_dates():
    if not NORMALIZED_FILE.exists():
        return set()
    df = pd.read_csv(NORMALIZED_FILE)
    if "Date" not in df.columns:
        return set()
    return set(df["Date"].astype(str).tolist())


def fetch_dominance_btc():
    """
    Fonte: CoinGecko /global
    Retorna dominância BTC em percentagem
    """
    url = "https://api.coingecko.com/api/v3/global"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["data"]["market_cap_percentage"]["btc"]


def append_row(date_str, dominance_value):
    row = pd.DataFrame(
        [{
            "Date": date_str,
            "DominanceBTC": float(dominance_value)
        }]
    )

    if NORMALIZED_FILE.exists():
        df = pd.read_csv(NORMALIZED_FILE)
        df = pd.concat([df, row], ignore_index=True)
    else:
        df = row

    df.to_csv(NORMALIZED_FILE, index=False)


# ------------------------------------------------------------
# MAIN LOOP (1 execução = 1 dia)
# ------------------------------------------------------------
def main():
    date_str = today_utc()
    existing_dates = load_existing_dates()

    if date_str in existing_dates:
        print(f"🟡 Dominance já registada para {date_str}")
        print("🧬 Organismo em silêncio.")
        return

    print(f"🧲 A recolher Dominance BTC para {date_str}")

    try:
        dominance = fetch_dominance_btc()
    except Exception as e:
        print(f"❌ Falha ao obter Dominance BTC: {e}")
        sys.exit(1)

    append_row(date_str, dominance)

    print("✅ Dominance diária registada com sucesso")
    print(f"📅 Date: {date_str}")
    print(f"📊 DominanceBTC: {dominance}")


# ------------------------------------------------------------
# ENTRYPOINT
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
