# CANONICAL JOBS — BITCOIN ORGANISM
Versão: 1.0
Estado: Ativo
Princípio: Tudo converge no Date (UTC, daily close)

────────────────────────────────────────────
JOB A — BTC DOMINANCE DIÁRIA (CANÓNICO)
────────────────────────────────────────────

Nome:
  collect + normalize BTC Dominance (daily)

Camadas:
  Layer 0 → Layer 1

Input:
  Fonte externa (CoinGecko / CoinMarketCap)
  Frequência: diária
  Timezone: UTC (daily close)

Pastas:
  raw/dominance/
  normalized/dominance_daily.csv

Output:
  Date, DominanceBTC

Regras:
  • Um dia = uma linha
  • Se falhar → log + não escreve
  • Nunca sobrescreve dados existentes
  • Append-only

Estado:
  Independente
  Estrutural
  Não especulativo

Pode correr:
  1x por dia após UTC close

Não pode:
  • Inventar valores
  • Preencher buracos automaticamente


────────────────────────────────────────────
JOB B — BTC OHLCV DIÁRIO (CANÓNICO)
────────────────────────────────────────────

Nome:
  collect + normalize BTC OHLCV (daily)

Camadas:
  Layer 0 → Layer 1

Input:
  Exchange primária (Binance)
  Granularidade: 1D
  Fecho: UTC

Pastas:
  raw/ohlcv/
  normalized/btc_ohlcv_daily.csv

Output:
  Date, Open, High, Low, Close, Volume

Regras:
  • Um dia = uma vela
  • Datas sempre UTC
  • Sem buracos temporais
  • Reprocessável a partir do RAW

Estado:
  Factual
  Mensurável
  Reversível

Pode correr:
  Diário após UTC close

Não pode:
  • Ajustar candles
  • Corrigir dados históricos manualmente


────────────────────────────────────────────
JOB C — FUSÃO DIÁRIA (MARKET + DOMINANCE)
────────────────────────────────────────────

Nome:
  fuse_daily_market_dominance

Camadas:
  Layer 2

Inputs:
  normalized/btc_ohlcv_daily.csv
  normalized/dominance_daily.csv

Output:
  fused/btc_daily_fused.csv

Schema:
  Date, Open, High, Low, Close, Volume, DominanceBTC

Regras críticas:
  • Join exclusivo por Date
  • Se Dominance faltar → NaN + flag
  • Nunca inventar dados
  • Uma linha = uma verdade diária

Estado:
  Integrador
  Sensível a falhas upstream

Pode correr:
  Após Job A e Job B

Não pode:
  • Reordenar datas
  • Preencher valores ausentes


────────────────────────────────────────────
AUTOMAÇÃO (AINDA NÃO ATIVA)
────────────────────────────────────────────

Scheduler:
  Desligado por defeito

Condição para ativação:
  • Jobs estáveis ≥ 30 dias
  • Logs limpos
  • Zero sobrescrita detectada

Princípio:
  Primeiro verdade.
  Depois repetição.
  Só no fim velocidade.
