import json
import hashlib
from pathlib import Path

print("🔐 OBSERVABILIDADE — CHECKSUMS CANÓNICOS")

# =========================================================
# PROJECT ROOT
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
METRICS_DIR = DATA_DIR / "metrics"
CHECKSUM_FILE = METRICS_DIR / "checksums.json"

FILES = {
    "btc_ohlcv_daily": DATA_DIR / "normalized" / "btc_ohlcv_daily.csv",
    "dominance_daily": DATA_DIR / "normalized" / "dominance_daily.csv",
    "btc_daily_fused": DATA_DIR / "fused" / "btc_daily_fused.csv",
}

METRICS_DIR.mkdir(parents=True, exist_ok=True)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

checksums = {}

for name, path in FILES.items():
    if path.exists():
        checksums[name] = {
            "file": str(path),
            "sha256": sha256(path)
        }
        print(f"✔️ {name} checksum calculado")
    else:
        checksums[name] = {
            "file": str(path),
            "sha256": None,
            "warning": "ficheiro inexistente"
        }
        print(f"⚠️ {name} não encontrado")

CHECKSUM_FILE.write_text(json.dumps(checksums, indent=2))

print("✅ Checksums atualizados com sucesso")
print(f"📄 {CHECKSUM_FILE}")
