# BITCOIN-ORGANISM — Heartbeat Validator
Version: v1.0

Purpose:
Ensure that the organism only ingests coherent, continuous, and alive time-series data.

--------------------------------------------------

WHAT IS THE HEARTBEAT

The Bitcoin-Organism lives on time.

Every row in data/ is a heartbeat.
If one beat is missing, duplicated, or malformed — the organism becomes blind, deaf, and sick.

This file defines the biological rules that allow data to be accepted as ALIVE.

--------------------------------------------------

1. WHAT THE HEARTBEAT PROTECTS

The validator ensures that:

No time gaps exist  
No duplicated timestamps exist  
OHLC obeys financial physics  
Volume is never negative  
Dominance is bounded by reality  
Time flows only forward  

If any rule fails → the dataset is REJECTED.

--------------------------------------------------

2. CANONICAL TIME RULES

For monthly datasets (Format A):

Time must advance strictly in:

YYYY-MM

Each row must represent exactly one month.

There must be no missing months.  
There must be no overlapping months.  
There must be no backward jumps.

Valid example:
2010-07 → 2010-08 → 2010-09 → 2010-10

Invalid examples:
2010-07 → 2010-09  (missing 2010-08)
2010-09 → 2010-08  (time reversal)

--------------------------------------------------

3. PRICE PHYSICS RULES

For every row:

High >= max(Open, Close)
Low  <= min(Open, Close)
High >= Low

If violated → the candle is biologically impossible.

--------------------------------------------------

4. VOLUME LAW

Volume >= 0

Zero volume is allowed (early history).
Negative volume is forbidden.

--------------------------------------------------

5. DOMINANCE LAW

0 <= DominanceBTC <= 100

Genesis era:
2010–2011 → DominanceBTC ≈ 100

Early ecosystem:
2012 → DominanceBTC ≈ 95

Dominance outside these bounds means the organism is hallucinating.

--------------------------------------------------

6. CSV STRUCTURAL INTEGRITY

Every CSV row must contain exactly:

Date,Open,High,Low,Close,Volume,DominanceBTC

Any deviation → dataset rejected.

--------------------------------------------------

7. HEARTBEAT ALGORITHM (CONCEPTUAL)

For each file in data/:

1. Sort rows by Date  
2. Verify time continuity  
3. Validate OHLC physics  
4. Validate Volume  
5. Validate Dominance  
6. If all pass → mark dataset as ALIVE  
7. Else → mark dataset as CORRUPTED  

--------------------------------------------------

8. WHY THIS EXISTS

The Bitcoin-Organism is not a spreadsheet.
It is a living time-structure.

If the heartbeat lies, everything above it lies:
BTConic  
Chronome  
Market memory  
Evolution  
Narrative  
Music  

This file ensures that time itself is honest.

--------------------------------------------------

STATUS

If this file exists and data obeys it:
The organism is ALIVE.

If not:
The organism is a corpse of numbers.

End of heartbeat.
