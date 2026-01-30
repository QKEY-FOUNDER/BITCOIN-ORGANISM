from pathlib import Path
import pandas as pd
from datetime import datetime

# ============================================================
# REGIME MEMORY ENGINE
# Memória canónica de regimes (mensal)
# ============================================================

class RegimeMemory:
    """
    Mantém memória de regimes consecutivos ao longo do tempo.
    Não escreve em dados de mercado.
    Apenas observa e recorda.
    """

    def __init__(self, snapshot_dir: Path, min_months: int = 3):
        """
        snapshot_dir : diretório com snapshots diários/mensais
        min_months   : número mínimo de meses consecutivos
                       para declarar um regime estável
        """
        self.snapshot_dir = snapshot_dir
        self.min_months = min_months

    # --------------------------------------------------------

    def _load_snapshots(self) -> pd.DataFrame:
        """
        Carrega snapshots JSON e extrai estado mensal.
        Espera campos:
        - date
        - canonical_state.macro
        - canonical_state.geo
        - immune.action
        """
        records = []

        for file in sorted(self.snapshot_dir.glob("*.json")):
            try:
                data = pd.read_json(file, typ="series")

                date = pd.to_datetime(data.get("date"))
                canonical = data.get("canonical_state", {})
                immune = data.get("immune", {})

                records.append({
                    "month": date.to_period("M"),
                    "macro": canonical.get("macro"),
                    "geo": canonical.get("geo"),
                    "immune_action": immune.get("action"),
                })

            except Exception:
                # silêncio absoluto: memória não interfere
                continue

        if not records:
            return pd.DataFrame()

        df = pd.DataFrame(records)
        df = df.dropna()
        return df

    # --------------------------------------------------------

    def compute_regimes(self) -> list:
        """
        Identifica regimes estáveis com base em
        meses consecutivos iguais.
        Retorna lista de regimes.
        """
        df = self._load_snapshots()

        if df.empty:
            return []

        regimes = []
        current = None
        count = 0

        for _, row in df.iterrows():
            key = (row["macro"], row["geo"], row["immune_action"])

            if key == current:
                count += 1
            else:
                if current and count >= self.min_months:
                    regimes.append({
                        "macro": current[0],
                        "geo": current[1],
                        "immune_action": current[2],
                        "months": count,
                    })
                current = key
                count = 1

        # último bloco
        if current and count >= self.min_months:
            regimes.append({
                "macro": current[0],
                "geo": current[1],
                "immune_action": current[2],
                "months": count,
            })

        return regimes

    # --------------------------------------------------------

    def current_regime(self):
        """
        Retorna o regime atual, se existir.
        """
        regimes = self.compute_regimes()
        if not regimes:
            return None
        return regimes[-1]
