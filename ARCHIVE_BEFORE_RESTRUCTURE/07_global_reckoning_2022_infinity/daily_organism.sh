#!/bin/bash

# ==========================================================
# BITCOIN-ORGANISM — CICLO DIÁRIO AUTÓNOMO
# Vida contínua | 1 batimento por dia
# ==========================================================

BASE_DIR="$HOME/organisms/BITCOIN-ORGANISM/data/07_global_reckoning_2022_infinity"
LOG_DIR="$BASE_DIR/logs"
DATE=$(date +"%Y-%m-%d")

mkdir -p "$LOG_DIR"

echo "🧬 DAILY ORGANISM — $DATE" >> "$LOG_DIR/daily.log"
echo "==========================================" >> "$LOG_DIR/daily.log"

cd "$BASE_DIR" || exit 1

# ----------------------------------------------------------
# 1️⃣ PILAR SANGUE — OHLCV
# ----------------------------------------------------------
echo "🩸 OHLCV — coleta diária" >> "$LOG_DIR/daily.log"
python3 engine/collectors/collect_btc_ohlcv_daily.py >> "$LOG_DIR/daily.log" 2>&1
python3 engine/collectors/normalize_btc_ohlcv_daily.py >> "$LOG_DIR/daily.log" 2>&1

# ----------------------------------------------------------
# 2️⃣ PILAR SANGUE — DOMINANCE (1 chamada / dia)
# ----------------------------------------------------------
echo "🩸 DOMINANCE — coleta diária" >> "$LOG_DIR/daily.log"
python3 engine/collectors/stream_btc_dominance_daily.py >> "$LOG_DIR/daily.log" 2>&1
python3 engine/collectors/normalize_btc_dominance_daily.py >> "$LOG_DIR/daily.log" 2>&1

# ----------------------------------------------------------
# 3️⃣ FUSÃO SANGUÍNEA
# ----------------------------------------------------------
echo "🧪 FUSÃO OHLCV + DOMINANCE" >> "$LOG_DIR/daily.log"
python3 engine/mergers/merge_daily_ohlcv_dominance.py >> "$LOG_DIR/daily.log" 2>&1

# ----------------------------------------------------------
# 4️⃣ VALIDAÇÕES
# ----------------------------------------------------------
echo "🛡️ VALIDAÇÕES" >> "$LOG_DIR/daily.log"
python3 engine/validators/validate_dominance_daily.py >> "$LOG_DIR/daily.log" 2>&1
python3 engine/validators/validate_daily_fused.py >> "$LOG_DIR/daily.log" 2>&1

# ----------------------------------------------------------
# 5️⃣ SISTEMA NERVOSO (STATE)
# ----------------------------------------------------------
echo "🧠 STATE ENGINE" >> "$LOG_DIR/daily.log"
python3 engine/state_engine/state_engine.py >> "$LOG_DIR/daily.log" 2>&1

# ----------------------------------------------------------
# 6️⃣ SISTEMA IMUNITÁRIO
# ----------------------------------------------------------
echo "🛡️ IMMUNE ENGINE" >> "$LOG_DIR/daily.log"
python3 engine/immune_system/immune_engine.py >> "$LOG_DIR/daily.log" 2>&1

# ----------------------------------------------------------
# 7️⃣ EXPRESSÃO VIVA
# ----------------------------------------------------------
echo "🎶 OUTPUT LAYER" >> "$LOG_DIR/daily.log"
python3 -m engine.output_layer.output_engine >> "$LOG_DIR/daily.log" 2>&1

echo "✅ Ciclo diário concluído — $DATE" >> "$LOG_DIR/daily.log"
echo "" >> "$LOG_DIR/daily.log"
