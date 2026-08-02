# Calibration Log — W30

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

## W30 Team Prediction vs Actual Result

| Target | Team Prediction | Predicted Direction | Predicted Range | Confidence | Actual Result | Actual Direction | Hit / Miss | Range Check | Score |
|---|---|---|---:|---|---:|---|---|---|---:|
| SPX | Down | down | -1.8% to +0.3% | Medium | +1.05% | up | MISS | Outside range | +0 |
| NDX | Down | down | -2.5% to +0.2% | High | +0.52% | up | MISS | Outside range | -2 |
| IWM | Neutral → Down | down | -1.8% to +0.5% | Medium | +0.01% | neutral | MISS | Inside range | +0 |
| XLK Technology | Down | down | -2.5% to +0.3% | High | -0.30% | down | HIT | Inside range | +3 |
| XLC Communication Services | Down | down | -2.0% to +0.4% | Medium | +1.83% | up | MISS | Outside range | +0 |
| XLY Consumer Discretionary | Down | down | -2.5% to +0.3% | High | +6.11% | up | MISS | Outside range | -2 |
| XLP Consumer Staples | Neutral | neutral | -0.7% to +0.8% | Medium | +1.09% | up | MISS | Outside range | +0 |
| XLE Energy | Neutral → Up | up | -0.5% to +2.0% | Medium | -0.12% | down | MISS | Inside range | +0 |
| XLF Financials | Neutral → Up | up | -0.5% to +1.3% | Medium | +1.12% | up | HIT | Inside range | +2 |
| XLV Health Care | Up | up | -0.3% to +1.5% | Medium | -0.01% | neutral | MISS | Inside range | +0 |
| XLI Industrials | Neutral → Up | up | -0.4% to +1.4% | Medium | -1.54% | down | MISS | Outside range | +0 |
| XLB Materials | Neutral | neutral | -1.0% to +0.8% | Medium | -1.62% | down | MISS | Outside range | +0 |
| XLRE Real Estate | Neutral → Up | up | -0.6% to +1.2% | Medium | -1.92% | down | MISS | Outside range | +0 |
| XLU Utilities | Up | up | -0.3% to +1.5% | Medium | -4.19% | down | MISS | Outside range | +0 |

---

## Calibration Summary

**Direction Result:** 2 HIT, 12 MISS
**Hit Rate:** 2 / 14 = 14.3%
**Working Calibration Score:** +1
**Structured Result File:** `calibration_result_W30.json`

---

## QA Comment

This calibration measures directional accuracy with confidence weighting. The range check is reported separately and does not change the official W22-style score.

Generated automatically at: 2026-08-02 07:41:24
