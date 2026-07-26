# Calibration Log — W29

## Role R10 — QA and Learning Log Lead

## Purpose

This file records how well the team’s market prediction matched the actual weekly market result. The calibration is generated automatically from the prediction file and the actuals file.

---

## Scoring Rules

The same scoring method from W22 is reused for consistency.

| Confidence Level | Prediction Result | Score |
|---|---|---:|
| High | Correct | +3 |
| Medium | Correct | +2 |
| Low / Uncertain | Correct | +1 |
| High | Wrong | -2 |
| Medium | Wrong | 0 |
| Low / Uncertain | Wrong | +1 |

---

## W29 Team Prediction vs Actual Result

| Target | Team Prediction | Predicted Direction | Predicted Range | Confidence | Actual Result | Actual Direction | Hit / Miss | Range Check | Score |
|---|---|---|---:|---|---:|---|---|---|---:|
| SPX | Neutral → Down | down | -1.0% to +0.3% | Medium | +0.55% | up | MISS | Outside range | +0 |
| NDX | Down | down | -1.8% to +0.2% | Medium | +1.42% | up | MISS | Outside range | +0 |
| IWM | Neutral → Down | down | -1.3% to +0.3% | Medium | -0.09% | down | HIT | Inside range | +2 |
| XLK Technology | Down | down | -2.0% to +0.3% | Medium | +2.67% | up | MISS | Outside range | +0 |
| XLC Communication Services | Neutral-Bearish | down | N/A | Medium | -1.31% | down | HIT | N/A | +2 |
| XLY Consumer Discretionary | Bearish | down | N/A | Medium | -1.23% | down | HIT | N/A | +2 |
| XLP Consumer Staples | Neutral-Bullish | up | N/A | Medium | -0.95% | down | MISS | N/A | +0 |
| XLE Energy | Up | up | +0.5% to +2.5% | Medium | +2.64% | up | HIT | Outside range | +2 |
| XLF Financials | Neutral | neutral | -0.5% to +1.0% | Medium | -0.37% | down | MISS | Inside range | +0 |
| XLV Health Care | Neutral | neutral | N/A | Medium | -1.03% | down | MISS | N/A | +0 |
| XLI Industrials | Neutral-Bearish | down | N/A | Medium | -0.31% | down | HIT | N/A | +2 |
| XLB Materials | Neutral → Down | down | -1.0% to +0.5% | Medium | +0.57% | up | MISS | Outside range | +0 |
| XLRE Real Estate | Neutral-Bullish | up | N/A | Medium | -0.90% | down | MISS | N/A | +0 |
| XLU Utilities | Neutral | neutral | -0.4% to +0.8% | Medium | +1.68% | up | MISS | Outside range | +0 |

---

## Calibration Summary

**Direction Result:** 5 HIT, 9 MISS
**Hit Rate:** 5 / 14 = 35.7%
**Working Calibration Score:** +10
**Structured Result File:** `calibration_result_W29.json`

---

## QA Comment

This calibration measures directional accuracy with confidence weighting. The range check is reported separately and does not change the official W22-style score.

Generated automatically at: 2026-07-26 07:39:28
