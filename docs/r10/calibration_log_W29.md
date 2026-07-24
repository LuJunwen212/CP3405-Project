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
| SPX | Neutral → Down | down | -1.0% to +0.3% | Medium | +0.69% | up | MISS | Outside range | +0 |
| NDX | Down | down | -1.8% to +0.2% | Medium | +1.97% | up | MISS | Outside range | +0 |
| IWM | Neutral → Down | down | -1.3% to +0.3% | Medium | +0.85% | up | MISS | Outside range | +0 |
| XLK Technology | Down | down | -2.0% to +0.3% | Medium | +2.96% | up | MISS | Outside range | +0 |
| XLC Communication Services | Neutral-Bearish | down | N/A | Medium | -0.56% | down | HIT | N/A | +2 |
| XLY Consumer Discretionary | Bearish | down | N/A | Medium | -0.49% | down | HIT | N/A | +2 |
| XLP Consumer Staples | Neutral-Bullish | up | N/A | Medium | -1.33% | down | MISS | N/A | +0 |
| XLE Energy | Up | up | +0.5% to +2.5% | Medium | +1.42% | up | HIT | Inside range | +2 |
| XLF Financials | Neutral | neutral | -0.5% to +1.0% | Medium | -0.27% | down | MISS | Inside range | +0 |
| XLV Health Care | Neutral | neutral | N/A | Medium | -0.52% | down | MISS | N/A | +0 |
| XLI Industrials | Neutral-Bearish | down | N/A | Medium | -0.42% | down | HIT | N/A | +2 |
| XLB Materials | Neutral → Down | down | -1.0% to +0.5% | Medium | -0.85% | down | HIT | Inside range | +2 |
| XLRE Real Estate | Neutral-Bullish | up | N/A | Medium | -0.48% | down | MISS | N/A | +0 |
| XLU Utilities | Neutral | neutral | -0.4% to +0.8% | Medium | -0.55% | down | MISS | Outside range | +0 |

---

## Calibration Summary

**Direction Result:** 5 HIT, 9 MISS
**Hit Rate:** 5 / 14 = 35.7%
**Working Calibration Score:** +10
**Structured Result File:** `calibration_result_W29.json`

---

## QA Comment

This calibration measures directional accuracy with confidence weighting. The range check is reported separately and does not change the official W22-style score.

Generated automatically at: 2026-07-22 10:44:53
