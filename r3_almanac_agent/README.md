# R3 Almanac Agent Automation

## Overview

The R3 Almanac Agent extracts seasonal market information from the **Stock Trader's Almanac 2026** PDF and generates structured inputs for the CP3405 forecasting pipeline.

The automation produces seasonal evidence for:

- `SPX` — S&P 500
- `NDX` — represented by NASDAQ Composite Almanac statistics as a documented seasonal proxy
- `IWM` — Russell 2000
- All 11 required S&P 500 sector ETF categories

The script generates JSON, CSV, and Markdown outputs from one validated report object. Invalid or incomplete data causes the workflow to fail before the outputs are committed.

## Repository Structure

```text
CP3405-Project/
├── .github/
│   └── workflows/
│       └── r3_almanac_pipeline.yml
│
├── r3_almanac_agent/
│   ├── r3_almanac_agent.py
│   ├── requirements.txt
│   ├── README.md
│   └── Stock Trader's Almanac 2026_L.pdf
│
└── outputs/
    └── R3/
        ├── almanac_agent_W30.json
        ├── almanac_agent_W30.csv
        └── almanac_agent_W30.md
```

The source PDF must remain inside `r3_almanac_agent/`. The script searches for a PDF whose filename begins with:

```text
Stock Trader's Almanac 2026
```

---

## Requirements

The workflow uses:

- Ubuntu GitHub Actions runner
- Python `3.10`
- `pypdf>=4.0.0`

Install the dependencies from the repository root:

```bash
pip install -r r3_almanac_agent/requirements.txt
```

Alternatively:

```bash
cd r3_almanac_agent
pip install -r requirements.txt
```

---

## Supported Assets

### Index Outputs

| Project ticker | Almanac source |
|---|---|
| `SPX` | S&P 500 |
| `NDX` | NASDAQ Composite, used as the NDX seasonal proxy |
| `IWM` | Russell 2000 |

### Sector Outputs

| Project ETF | Project sector | Almanac ticker | Almanac category | Signal selected |
|---|---|---|---|---|
| `XLK` | Technology | `S5INFT` | InfoTech | Long |
| `XLU` | Utilities | `UTY` | Utilities | Long |
| `XLF` | Financials | `BKX` | Banking | Short |
| `XLE` | Energy | `XOI` | Oil | Short |
| `XLB` | Materials | `S5MATR` | Materials | Short |
| `XLY` | Consumer Discretionary | `S5COND` | Consumer Discretionary | Long |
| `XLP` | Consumer Staples | `S5CONS` | Consumer Staples | Long |
| `XLV` | Health Care | `S5HLTH` | HealthCare | Long |
| `XLI` | Industrials | `S5INDU` | Industrials | Long |
| `XLC` | Communication Services | `XTC` | Telecom | Long |
| `XLRE` | Real Estate | `RMZ` | Real Estate | Long |

The project ETF names are downstream identifiers. The actual seasonal rows are extracted from the corresponding Almanac series listed above.

---

## Automatic Week and Forecast-Date Logic

When no command-line arguments or workflow inputs are supplied, the script calculates:

1. The current ISO week number for the output filename.
2. The Monday-to-Friday period of the following week for the forecast date range.

Example:

```text
Workflow execution week: W30
Forecast target: following Monday to Friday
```

Generated filenames use the execution week:

```text
outputs/R3/almanac_agent_W30.json
outputs/R3/almanac_agent_W30.csv
outputs/R3/almanac_agent_W30.md
```

The week identifier and date range have different purposes:

- `W30` identifies the week when the report was generated.
- The date range identifies the future market week being forecast.

Command-line values take priority over automatic values.

---

## Local Execution

### Automatic Run

From the repository root:

```bash
python r3_almanac_agent/r3_almanac_agent.py
```

The script automatically determines the current ISO week and the following Monday-to-Friday forecast period.

### Manual Run

```bash
python r3_almanac_agent/r3_almanac_agent.py W30 "2026-07-27 to 2026-07-31"
```

On Windows PowerShell, the same command can be used:

```powershell
python r3_almanac_agent/r3_almanac_agent.py W30 "2026-07-27 to 2026-07-31"
```

Manual input requirements:

- Week format: `W` followed by two digits, such as `W30`
- Date format: `YYYY-MM-DD to YYYY-MM-DD`
- Start date: Monday
- End date: Friday
- Total range: five calendar days from Monday through Friday

---

## GitHub Actions Workflow

The workflow file is:

```text
.github/workflows/r3_almanac_pipeline.yml
```

Workflow name:

```text
R3 Almanac Agent Multi-Week Automation Pipeline
```

The workflow performs these stages:

1. Checks out the active repository branch.
2. Sets up Python 3.10.
3. Installs dependencies from `r3_almanac_agent/requirements.txt`.
4. Executes the R3 Python script.
5. Verifies that the JSON, CSV, and Markdown outputs exist and are non-empty.
6. Searches the generated outputs for invalid values.
7. Stages changed files from `outputs/R3/`.
8. Commits and pushes changed outputs to the active branch.
9. Creates no commit when the generated files are unchanged.

The workflow has:

```yaml
permissions:
  contents: write
```

This permission is required for the automation bot to commit and push generated outputs.

---

## Scheduled Run

The current cron configuration is:

```yaml
schedule:
  - cron: '0 0 * * 6'
```

GitHub Actions cron expressions use UTC.

| Time zone | Run time |
|---|---|
| UTC | Saturday at 01:13 |
| Singapore Time (UTC+8) | Saturday at 09:13 |

The scheduled run uses automatic values:

- Output week: current ISO week
- Forecast date range: following Monday to Friday

No manual input is required for the scheduled run.

Scheduled GitHub Actions workflows run from the repository's default branch. Therefore, the production workflow file must be present on the default branch for the Saturday schedule to execute.

---

## Manual GitHub Actions Run

The workflow also supports `workflow_dispatch`.

### Steps

1. Open the repository on GitHub.
2. Select **Actions**.
3. Select **R3 Almanac Agent Multi-Week Automation Pipeline**.
4. Select **Run workflow**.
5. Select the required branch.
6. Enter the optional week and date range.
7. Start the workflow.

### Inputs

#### `custom_market_week`

Manual output week override.

Example:

```text
W30
```

#### `custom_market_date`

Manual forecast date-range override.

Example:

```text
2026-07-27 to 2026-07-31
```

Both fields can be left blank. Blank values cause the Python script to use its automatic week and next-week date calculations.

---

## Generated Outputs

All outputs are written to:

```text
outputs/R3/
```

### JSON

```text
outputs/R3/almanac_agent_W30.json
```

Contains the full structured report:

- Agent identity
- Execution week
- Forecast date range
- Generation timestamp
- Source PDF
- Midterm election cycle context
- Monthly index statistics
- Weekly Almanac evidence
- Sector seasonality signals
- Evidence page numbers
- Extraction methods
- Almanac bias
- Confidence
- Tactical thesis

JSON generation uses:

```python
allow_nan=False
```

This prevents Python from publishing non-standard NaN or infinity values.

### CSV

```text
outputs/R3/almanac_agent_W30.csv
```

Contains flattened records for downstream processing.

Record categories:

- `index_stat`
- `sector_signal`
- `week_pattern`

### Markdown

```text
outputs/R3/almanac_agent_W30.md
```

Contains a human-readable report with:

- Execution and forecast context
- Monthly index statistics
- Weekly calendar evidence
- Complete 11-sector seasonality matrix
- Almanac bias
- Confidence
- Tactical thesis

All three files are generated from the same validated report object.

---

## Almanac Bias and Confidence

The script derives its bias from the three extracted midterm-year index returns:

- SPX
- NDX proxy
- IWM

Bias rules:

| Average midterm return | Bias |
|---|---|
| `>= +0.5` | Bullish |
| `<= -0.5` | Bearish |
| Between `-0.5` and `+0.5` | Neutral |

Confidence rules:

| Direction agreement | Confidence |
|---|---|
| All three returns have the same direction | High |
| Two of three returns have the same direction | Medium |
| No directional majority | Low |

---

## Validation Rules

Validation runs before any output file is written.

The report must contain exactly:

```text
SPX
NDX
IWM
```

It must also contain exactly the 11 required sector ETFs:

```text
XLK
XLU
XLF
XLE
XLB
XLY
XLP
XLV
XLI
XLC
XLRE
```

The validator rejects:

- NaN
- Positive or negative infinity
- `None`
- `null`
- Blank required strings
- `N/A`
- `NA`
- Invalid week formats
- Invalid dates
- Non-Monday start dates
- Non-Friday end dates
- Date ranges other than Monday to Friday
- Missing indices
- Unexpected indices
- Missing sectors
- Unexpected sectors
- Invalid or missing source pages
- Invalid percentage formats
- Signals other than `LONG` or `SHORT`
- Extraction methods containing `fallback`

Valid percentage examples:

```text
+1.3%
-0.8%
+10.66%
```

Invalid examples:

```text
1.3
1.3%
NaN
N/A
null
infinity
```

---

## Extraction Failure Behaviour

The script does not publish fallback estimates.

If the required Almanac table or sector row cannot be extracted, the script raises an error and stops.

Example:

```text
ValueError: R3 sector extraction failed.
Missing required rows: XLP (S5CONS, Consumer Staples, Long)
```

When extraction or validation fails:

1. The Python process exits with a non-zero status.
2. The GitHub Actions execution step fails.
3. Output writing does not begin.
4. Existing valid files remain unchanged.
5. The verification and commit steps do not publish invalid outputs.

---

## Workflow Output Verification

After the Python script succeeds, the workflow independently verifies all three output files:

```text
outputs/R3/almanac_agent_<WEEK>.json
outputs/R3/almanac_agent_<WEEK>.csv
outputs/R3/almanac_agent_<WEEK>.md
```

Each file must:

- Exist
- Be non-empty
- Contain no detected `nan`
- Contain no detected `null`
- Contain no detected `n/a`
- Contain no detected `infinity`

Successful verification prints:

```text
All R3 artifacts exist and passed verification.
```

A missing, empty, or invalid output causes the workflow to fail.

---

## Automatic Commit Behaviour

The workflow stages:

```bash
git add outputs/R3/
```

If the regenerated outputs differ from the repository versions, it commits them using:

```text
Team 2 Almanac Automation Bot
```

Commit message:

```text
chore(data): automated R3 next-week forecast execution matrix [skip ci]
```

The `[skip ci]` marker prevents the generated-output commit from triggering an unnecessary additional CI run.

If no staged changes exist, the workflow prints:

```text
No strategic data shifts detected. Terminating smoothly.
```

and does not create an empty commit.

The workflow pushes to the branch on which it is running.

---

## Testing

### Valid Local Test

```bash
python r3_almanac_agent/r3_almanac_agent.py W30 "2026-07-27 to 2026-07-31"
```

Expected messages include:

```text
R3 validation passed: 3 indices, 11 sectors, valid dates and no invalid values.
Successfully compiled all unified artifacts
```

### Valid GitHub Actions Test

Run the workflow manually with:

```text
W30
2026-07-27 to 2026-07-31
```

Confirm:

- The workflow succeeds.
- All three output files are generated.
- Verification succeeds.
- Changed outputs are committed automatically.
- No unnecessary commit is created when the files are unchanged.

### NaN Failure Test

For a controlled validation test only, temporarily insert this after `build_report()` and before `validate_report()`:

```python
report["sector_signals"]["XLK"]["average_return_25_year"] = float("nan")
```

Expected result:

```text
ValueError: R3 report validation failed:
- report.sector_signals.XLK.average_return_25_year contains NaN or infinity.
```

For GitHub Actions evidence, perform this test on a temporary test branch.

The NaN injection must be removed after testing and must not be merged into the production branch.

---

## Troubleshooting

### PDF Not Found

Error:

```text
FileNotFoundError: Missing baseline database asset
```

Check that the Almanac PDF is located inside:

```text
r3_almanac_agent/
```

### Missing Sector Row

Error:

```text
R3 sector extraction failed. Missing required rows
```

Check:

- `pdf_ticker`
- `pdf_sector`
- `desired_type`
- Almanac table text extraction

Do not add fallback values to bypass the failure.

### Invalid Date Range

Required format:

```text
YYYY-MM-DD to YYYY-MM-DD
```

The date range must start on Monday and end on Friday.

### Workflow Succeeds but No Commit Appears

This is expected when the new outputs are identical to the existing repository files.

Check the workflow log for:

```text
No strategic data shifts detected. Terminating smoothly.
```

### Push Permission Failure

Confirm that the workflow includes:

```yaml
permissions:
  contents: write
```

Also confirm that repository Actions settings allow GitHub Actions to write repository contents.

### Scheduled Workflow Does Not Run

Check that:

- The workflow file is present on the default branch.
- GitHub Actions is enabled for the repository.
- The cron schedule remains active.
- The workflow has not been disabled due to repository inactivity.

---

## Downstream Handoff

The authoritative R3 output directory is:

```text
outputs/R3/
```

Downstream roles and automation should no longer reference:

```text
r3_almanac_agent/outputs/
```

R7, R8, R9, and pipeline verification logic should use the repository-level R3 output path.
