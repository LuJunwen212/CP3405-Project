# R3 Almanac Agent

## Sprint 8 / W30

The R3 automation extracts seasonal market evidence from the Stock
Trader's Almanac 2026 and produces structured outputs for:

- SPX
- NDX using NASDAQ Composite as the documented seasonal proxy
- IWM
- All 11 S&P 500 sector ETF categories

## Output location

outputs/R3/

## W30 outputs

- almanac_agent_W30.json
- almanac_agent_W30.csv
- almanac_agent_W30.md

## Manual execution

python r3_almanac_agent/r3_almanac_agent.py W30 \
  "2026-07-27 to 2026-07-31"

## Validation

The automation fails before writing files when it detects:

- NaN or infinity
- Null or blank values
- Invalid dates
- Missing indices or sectors
- Invalid percentage formats
- Failed PDF extraction
- Fallback or estimated data