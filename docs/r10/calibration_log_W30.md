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
| SPX | ** Down **Expected | down | ** -1.8% to +0.3% ** | Medium | +0.02% | down | HIT | Inside range | +2 |
| NDX | ** Down **Expected | down | ** -2.5% to +0.2% ** | Medium | -0.32% | down | HIT | Inside range | +2 |
| IWM | ** Neutral → Down **Expected | down | ** -1.8% to +0.5% ** | Medium | +0.60% | up | MISS | Outside range | +0 |

---

## Calibration Summary

**Direction Result:** 2 HIT, 1 MISS
**Hit Rate:** 2 / 3 = 66.7%
**Working Calibration Score:** +4
**Structured Result File:** `calibration_result_W30.json`

---

## Automation Warnings

Missing predictions: XLK, XLC, XLY, XLP, XLE, XLF, XLV, XLI, XLB, XLRE, XLU

---

## QA Comment

This calibration measures directional accuracy with confidence weighting. The range check is reported separately and does not change the official W22-style score.

Generated automatically at: 2026-07-29 13:04:17
