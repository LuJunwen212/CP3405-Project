# Calibration Log — W28

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

## W28 Team Prediction vs Actual Result

| Target | Team Prediction | Predicted Direction | Predicted Range | Confidence | Actual Result | Actual Direction | Hit / Miss | Range Check | Score |
|---|---|---|---:|---|---:|---|---|---|---:|
| SPX | Up | up | +0.4% to +1.4% | Medium | -1.55% | down | MISS | Outside range | +0 |
| NDX | Neutral → Up | up | +0.2% to +1.3% | Medium | -4.13% | down | MISS | Outside range | +0 |
| IWM | Up | up | +0.5% to +1.6% | Medium | -0.66% | down | MISS | Outside range | +0 |
| XLK Technology | Up | up | +1.0% to +2.5% | High | -5.48% | down | MISS | Outside range | -2 |
| XLC Communication Services | Neutral-Bullish | up | N/A | Medium | -0.89% | down | MISS | N/A | +0 |
| XLY Consumer Discretionary | Neutral-Bullish | up | N/A | Medium | -1.54% | down | MISS | N/A | +0 |
| XLP Consumer Staples | Neutral | neutral | N/A | Medium | +1.27% | up | MISS | N/A | +0 |
| XLE Energy | Neutral → Up | up | -0.3% to +1.3% | Medium | +4.72% | up | HIT | Outside range | +2 |
| XLF Financials | Neutral → Up | up | 0.0% to +1.2% | Medium | +0.99% | up | HIT | Inside range | +2 |
| XLV Health Care | Neutral | neutral | N/A | Medium | +0.16% | up | MISS | N/A | +0 |
| XLI Industrials | Neutral-Bullish | up | N/A | Medium | -1.38% | down | MISS | N/A | +0 |
| XLB Materials | Neutral → Up | up | -0.2% to +1.1% | Medium | -0.71% | down | MISS | Outside range | +0 |
| XLRE Real Estate | Neutral | neutral | N/A | Medium | +2.18% | up | MISS | N/A | +0 |
| XLU Utilities | Neutral | neutral | -0.4% to +0.8% | Medium | -0.53% | down | MISS | Outside range | +0 |

---

## Calibration Summary

**Direction Result:** 2 HIT, 12 MISS
**Hit Rate:** 2 / 14 = 14.3%
**Working Calibration Score:** +2
**Structured Result File:** `calibration_result_W28.json`

---

## QA Comment

This calibration measures directional accuracy with confidence weighting. The range check is reported separately and does not change the official W22-style score.

Generated automatically at: 2026-07-18 05:08:20
