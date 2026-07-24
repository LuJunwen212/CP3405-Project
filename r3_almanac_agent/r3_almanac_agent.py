#!/usr/bin/env python3
"""
R3 Almanac Agent Automation - Production Forecasting Version
Decoupled architecture: Generates filenames under the CURRENT runtime week (e.g., W29)
while internally accelerating the data range by +7 days to forecast the NEXT trading week.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import datetime
import math
from pathlib import Path
from typing import Any

# ========================================================
# 1. Dynamic Parameter Initialization with Separated Run-Week and Forecast-Dates
# ========================================================
# A. Current Execution Week Node (Determines File Output Names & Global Structural Anchors)
today = datetime.date.today()
automated_current_week = f"W{today.strftime('%V')}"  # Resolves dynamically to W29 on July 14, 2026

# B. Target Forecast Node (Determines Internal Prediction Date Range Shifted +7 Days)
forecast_target_day = today + datetime.timedelta(days=7)
next_week_monday = forecast_target_day - datetime.timedelta(days=forecast_target_day.weekday())
next_week_friday = next_week_monday + datetime.timedelta(days=4)
automated_date_range = f"{next_week_monday.strftime('%Y-%m-%d')} to {next_week_friday.strftime('%Y-%m-%d')}"  # 2026-07-20 to 2026-07-24

# Priority Logic Chain: 1. CLI Override parameters (Manual Triggers) > 2. Automated Next-Week Forecast Rolling
WEEK = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else automated_current_week
DATE_RANGE = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip() else automated_date_range
AGENT = "R3 Almanac Agent"

print(f"--- R3 ENGINE INITIALIZED ---")
print(f"Report Run Week (File Identity) : {WEEK}")
print(f"Target Forecast Date Range      : {DATE_RANGE}")

# Dynamic Month Detection logic to prevent crashing on month transitions
def detect_month(date_range: str) -> str:
    match = re.fullmatch(
        r"(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})",
        date_range,
    )

    if not match:
        raise ValueError(
            "Invalid date range. Expected format: "
            "YYYY-MM-DD to YYYY-MM-DD"
        )

    try:
        start_date = datetime.date.fromisoformat(match.group(1))
        datetime.date.fromisoformat(match.group(2))
    except ValueError as exc:
        raise ValueError(
            f"Invalid calendar date in date range: {date_range}"
        ) from exc

    return start_date.strftime("%B").upper()

TARGET_MONTH = detect_month(DATE_RANGE)

# Fully expanded matrix covering all 11 core Global Industry Classification Standard (GICS) sectors
SECTOR_REQUESTS = {
    "XLK": {"pdf_ticker": "S5INFT", "pdf_sector": "InfoTech", "project_sector": "Technology", "desired_type": "Long"},
    "XLU": {"pdf_ticker": "UTY", "pdf_sector": "Utilities", "project_sector": "Utilities", "desired_type": "Long"},
    "XLF": {"pdf_ticker": "BKX", "pdf_sector": "Banking", "project_sector": "Financials", "desired_type": "Short"},
    "XLE": {"pdf_ticker": "XOI", "pdf_sector": "Oil", "project_sector": "Energy", "desired_type": "Short"},
    "XLB": {"pdf_ticker": "S5MATR", "pdf_sector": "Materials", "project_sector": "Materials", "desired_type": "Short"},
    "XLY": {"pdf_ticker": "S5COND", "pdf_sector": "Consumer Discretionary", "project_sector": "Consumer Discretionary", "desired_type": "Long"},
    "XLP": {"pdf_ticker": "S5CONS", "pdf_sector": "Consumer Staples", "project_sector": "Consumer Staples", "desired_type": "Long"},
    "XLV": {"pdf_ticker": "S5HLTH", "pdf_sector": "HealthCare", "project_sector": "Health Care", "desired_type": "Long"},
    "XLI": {"pdf_ticker": "S5INDU", "pdf_sector": "Industrials", "project_sector": "Industrials", "desired_type": "Long"},
    "XLC": {"pdf_ticker": "XTC", "pdf_sector": "Telecom", "project_sector": "Communication Services", "desired_type": "Long"},
    "XLRE": {"pdf_ticker": "RMZ", "pdf_sector": "Real Estate", "project_sector": "Real Estate", "desired_type": "Long"},
}

REQUIRED_INDICES = {"SPX", "NDX", "IWM"}
REQUIRED_SECTORS = set(SECTOR_REQUESTS)

PERCENT_PATTERN = re.compile(r"^[+-]\d+(?:\.\d+)?%$")

INVALID_TEXT_VALUES = {
    "",
    "nan",
    "null",
    "none",
    "n/a",
    "na",
    "inf",
    "+inf",
    "-inf",
    "infinity",
    "+infinity",
    "-infinity",
}

def script_folder() -> Path:
    return Path(__file__).resolve().parent

def find_pdf(folder: Path) -> Path:
    pdfs = list(folder.glob("*.pdf")) + list(folder.glob("**/Stock Trader's Almanac 2026*.pdf"))
    if not pdfs:
        raise FileNotFoundError("Missing baseline database asset: Stock Trader's Almanac 2026_L.pdf")
    
    exact_names = ["Stock Trader's Almanac 2026_L.pdf", "Stock Trader's Almanac 2026_L(2).pdf"]
    for name in exact_names:
        for pdf in pdfs:
            if pdf.name == name:
                return pdf
    return pdfs[0]

def read_pdf_pages(pdf_path: Path) -> list[dict[str, Any]]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ImportError("Missing structural dependency. Please run: pip install pypdf") from exc

    reader = PdfReader(str(pdf_path))
    pages: list[dict[str, Any]] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append({"page_number": i, "text": text})
    return pages

def normalize_minus(value: str) -> str:
    return value.replace("–", "-").replace("−", "-")

def format_percent(value: str) -> str:
    value = normalize_minus(value.strip())
    if value.startswith("-"):
        return f"{value}%"
    return f"+{value}%"

def percent_to_float(value: str) -> float:
    normalized = normalize_minus(value).replace("%", "").strip()
    return float(normalized)


def derive_index_outlook(
    monthly_stats: dict[str, Any],
    month: str,
) -> tuple[str, str]:
    month_key = month.lower()
    return_key = f"midterm_{month_key}_average_return"

    returns = [
        percent_to_float(item[return_key])
        for item in monthly_stats.values()
    ]

    average_return = sum(returns) / len(returns)
    positive_count = sum(value > 0 for value in returns)
    negative_count = sum(value < 0 for value in returns)

    if average_return >= 0.5:
        bias = "Bullish"
    elif average_return <= -0.5:
        bias = "Bearish"
    else:
        bias = "Neutral"

    if positive_count == len(returns) or negative_count == len(returns):
        confidence = "HIGH"
    elif positive_count >= 2 or negative_count >= 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return bias, confidence

def find_page(pages: list[dict[str, Any]], include: list[str], exclude: list[str] | None = None) -> dict[str, Any]:
    exclude = exclude or []
    for page in pages:
        text = page["text"].upper()
        if all(term.upper() in text for term in include) and not any(term.upper() in text for term in exclude):
            return page
    raise ValueError(f"Could not automatically isolate PDF page matching parameters: {include}")

def extract_vital_statistics(
    pages: list[dict[str, Any]],
    month: str,
) -> dict[str, Any]:
    m_lower = month.lower()

    page = find_page(
        pages,
        include=[
            f"{month} ALMANAC",
            f"{month.capitalize()} Vital Statistics",
            "Average % Change",
        ],
        exclude=["TABLE OF CONTENTS"],
    )

    text = re.sub(r"\s+", " ", page["text"])

    rank_match = re.search(
        r"Rank\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
        text,
    )
    avg_match = re.search(
        r"Average % Change\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)",
        text,
    )
    midterm_match = re.search(
        r"Midterm Yr Avg % Chg\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)\s+"
        r"([–−-]?\d+\.\d+)",
        text,
    )

    if not rank_match:
        raise ValueError(
            f"R3 extraction failed: {month} rank row not found "
            f"on PDF page {page['page_number']}."
        )

    if not avg_match:
        raise ValueError(
            f"R3 extraction failed: {month} average-return row not found "
            f"on PDF page {page['page_number']}."
        )

    if not midterm_match:
        raise ValueError(
            f"R3 extraction failed: {month} midterm-return row not found "
            f"on PDF page {page['page_number']}."
        )

    columns = ["DJIA", "SPX", "NDX", "RUSSELL_1000", "IWM"]
    names = {
        "DJIA": "Dow Jones Industrial Average",
        "SPX": "S&P 500",
        "NDX": "NASDAQ Composite — used as NDX seasonal proxy",
        "RUSSELL_1000": "Russell 1000",
        "IWM": "Russell 2000",
    }

    ranks = rank_match.groups()
    averages = avg_match.groups()
    midterms = midterm_match.groups()

    result: dict[str, Any] = {}

    for index, ticker in enumerate(columns):
        result[ticker] = {
            "index": names[ticker],
            f"{m_lower}_rank": int(ranks[index]),
            f"normal_{m_lower}_average_return": format_percent(
                averages[index]
            ),
            f"midterm_{m_lower}_average_return": format_percent(
                midterms[index]
            ),
            "source_page": page["page_number"],
            "extraction_method":
                f"parsed_from_{m_lower}_vital_statistics_table",
        }

    return {
        "SPX": result["SPX"],
        "NDX": result["NDX"],
        "IWM": result["IWM"],
    }

def extract_dynamic_weekly_pattern(
    pages: list[dict[str, Any]],
    month: str,
    current_week: str,
) -> dict[str, Any]:
    page = find_page(
        pages,
        include=[f"{month} 2026"],
        exclude=["STRATEGY CALENDAR"],
    )

    text = re.sub(r"\s+", " ", page["text"]).strip()

    if not text:
        raise ValueError(
            f"R3 weekly-pattern extraction failed: "
            f"{month} 2026 planner text is empty."
        )

    return {
        "name": f"Dynamic Weekly Boundary Matrix ({current_week})",
        "evidence":
            f"{month.capitalize()} 2026 weekly planner source located.",
        "source_page": page["page_number"],
        "extraction_method":
            "parameterized_weekly_planner_extraction",
        "interpretation":
            "Seasonal planner evidence was located for the "
            "forecast-month context.",
    }

def compact_window(start_month: str, start_part: str, finish_month: str, finish_part: str) -> str:
    part_map = {"B": "Early", "M": "Mid", "E": "Late"}
    return f"{part_map.get(start_part, start_part)} {start_month} to {part_map.get(finish_part, finish_part)} {finish_month}"

def extract_sector_table_rows(
    pages: list[dict[str, Any]],
) -> dict[str, Any]:
    table_page = find_page(
        pages,
        include=[
            "SECTOR INDEX SEASONALITY TABLE",
            "Average % Return",
        ],
    )

    candidate_pages = [table_page]

    next_page = next(
        (
            page
            for page in pages
            if page["page_number"] == table_page["page_number"] + 1
        ),
        None,
    )

    if next_page is not None:
        candidate_pages.append(next_page)

    month_pattern = (
        r"January|February|March|April|May|June|"
        r"July|August|September|October|November|December"
    )
    number_pattern = r"[–−-]?\d+(?:\.\d+)?"

    extracted: dict[str, Any] = {}
    missing_sectors: list[str] = []

    for project_ticker, request in SECTOR_REQUESTS.items():
        pdf_ticker = request["pdf_ticker"]
        desired_type = request["desired_type"]

        # Allows multi-word names such as Consumer Discretionary
        # and Real Estate.
        sector_pattern = r"\s+".join(
            re.escape(part)
            for part in request["pdf_sector"].split()
        )

        row_pattern = re.compile(
            rf"\b{re.escape(pdf_ticker)}\b\s+"
            rf"(?P<pdf_sector>{sector_pattern})\s+"
            rf"{re.escape(desired_type)}\s+"
            rf"(?P<start_month>{month_pattern})\s+"
            rf"(?P<start_part>[BME])\s+"
            rf"(?P<finish_month>{month_pattern})\s+"
            rf"(?P<finish_part>[BME])\s+"
            rf"(?P<avg25>{number_pattern})\s+"
            rf"(?P<avg10>{number_pattern})\s+"
            rf"(?P<avg5>{number_pattern})\b",
            re.IGNORECASE,
        )

        match = None
        source_page = None

        for page in candidate_pages:
            normalized_text = re.sub(
                r"\s+",
                " ",
                page["text"],
            ).strip()

            match = row_pattern.search(normalized_text)

            if match:
                source_page = page["page_number"]
                break

        if match is None or source_page is None:
            missing_sectors.append(
                f"{project_ticker} "
                f"({pdf_ticker}, {request['pdf_sector']}, {desired_type})"
            )
            continue

        values = match.groupdict()

        extracted[project_ticker] = {
            "project_ticker": project_ticker,
            "project_sector": request["project_sector"],
            "pdf_ticker": pdf_ticker,
            "pdf_sector": values["pdf_sector"],
            "signal": desired_type.upper(),
            "seasonal_window": compact_window(
                values["start_month"],
                values["start_part"],
                values["finish_month"],
                values["finish_part"],
            ),
            "average_return_25_year": format_percent(
                values["avg25"]
            ),
            "average_return_10_year": format_percent(
                values["avg10"]
            ),
            "average_return_5_year": format_percent(
                values["avg5"]
            ),
            "source_page": source_page,
            "extraction_method":
                "parsed_from_sector_index_seasonality_table",
        }

    if missing_sectors:
        raise ValueError(
            "R3 sector extraction failed. Missing required rows: "
            + ", ".join(missing_sectors)
        )

    return extracted

def build_report(pdf_path: Path, pages: list[dict[str, Any]]) -> dict[str, Any]:
    monthly_stats = extract_vital_statistics(pages, TARGET_MONTH)
    week_pattern = extract_dynamic_weekly_pattern(pages, TARGET_MONTH, WEEK)
    sector_signals = extract_sector_table_rows(pages)

    current_bias, current_confidence = derive_index_outlook(monthly_stats, TARGET_MONTH)

    return {
        "agent": AGENT,
        "week": WEEK,
        "date_range": DATE_RANGE,
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "source_file": pdf_path.name,
        "automation_level": "Fully optimized parameterized pipeline output via Cloud Workflow infrastructure.",
        "cycle_context": {
            "year": "2026",
            "cycle": "U.S. midterm election year",
            "summary": f"Contextual baseline analyzed dynamically for the forecast month of {TARGET_MONTH.capitalize()}.",
        },
        "monthly_vital_statistics": monthly_stats,
        "week_specific_pattern": week_pattern,
        "sector_signals": sector_signals,
        "almanac_bias": current_bias,
        "confidence": current_confidence,
        "thesis": f"Strategic seasonal intelligence evaluation compiled in week {WEEK}. Internal data models capture predictive trading matrix signals for target duration {DATE_RANGE} under {TARGET_MONTH.capitalize()} systemic cycles.",
    }

def validate_report(report: dict[str, Any]) -> None:
    errors: list[str] = []
    month_key = TARGET_MONTH.lower()

    def check_page(value: Any, path: str) -> None:
        if not isinstance(value, int) or value <= 0:
            errors.append(f"{path} must be a positive integer.")

    def check_percent(value: Any, path: str) -> None:
        if not isinstance(value, str) or not PERCENT_PATTERN.fullmatch(value):
            errors.append(
                f"{path} must use percentage format such as +1.2% or -0.5%."
            )

    def scan_invalid_values(value: Any, path: str) -> None:
        if value is None:
            errors.append(f"{path} contains null/None.")
            return

        if isinstance(value, float) and not math.isfinite(value):
            errors.append(f"{path} contains NaN or infinity.")
            return

        if isinstance(value, str):
            if value.strip().lower() in INVALID_TEXT_VALUES:
                errors.append(f"{path} contains invalid text value: {value!r}.")
            return

        if isinstance(value, dict):
            for key, child in value.items():
                scan_invalid_values(child, f"{path}.{key}")
            return

        if isinstance(value, list):
            for index, child in enumerate(value):
                scan_invalid_values(child, f"{path}[{index}]")

    # Reject NaN, null, blank and equivalent values anywhere in the report.
    scan_invalid_values(report, "report")

    # Validate report identity.
    if report.get("agent") != AGENT:
        errors.append("Report agent name is missing or incorrect.")

    week = report.get("week")
    if not isinstance(week, str) or not re.fullmatch(r"W\d{2}", week):
        errors.append("Week must use two-digit format such as W30.")

    # Validate forecast date range.
    date_range = report.get("date_range")
    date_match = (
        re.fullmatch(
            r"(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})",
            date_range,
        )
        if isinstance(date_range, str)
        else None
    )

    if not date_match:
        errors.append(
            "Date range must use YYYY-MM-DD to YYYY-MM-DD format."
        )
    else:
        try:
            start_date = datetime.date.fromisoformat(date_match.group(1))
            end_date = datetime.date.fromisoformat(date_match.group(2))

            if start_date.weekday() != 0:
                errors.append("Forecast start date must be a Monday.")

            if end_date.weekday() != 4:
                errors.append("Forecast end date must be a Friday.")

            if end_date - start_date != datetime.timedelta(days=4):
                errors.append(
                    "Forecast range must cover one Monday-to-Friday week."
                )
        except ValueError:
            errors.append("Date range contains an invalid calendar date.")

    # Validate the three required indices.
    index_stats = report.get("monthly_vital_statistics")

    if not isinstance(index_stats, dict):
        errors.append("monthly_vital_statistics must be an object.")
    else:
        actual_indices = set(index_stats)

        if actual_indices != REQUIRED_INDICES:
            missing = REQUIRED_INDICES - actual_indices
            extra = actual_indices - REQUIRED_INDICES

            if missing:
                errors.append(
                    f"Missing required indices: {sorted(missing)}."
                )

            if extra:
                errors.append(
                    f"Unexpected indices found: {sorted(extra)}."
                )

        for ticker in REQUIRED_INDICES & actual_indices:
            item = index_stats[ticker]
            rank_key = f"{month_key}_rank"
            normal_key = f"normal_{month_key}_average_return"
            midterm_key = f"midterm_{month_key}_average_return"

            rank = item.get(rank_key)
            if not isinstance(rank, int) or not 1 <= rank <= 12:
                errors.append(
                    f"monthly_vital_statistics.{ticker}.{rank_key} "
                    "must be an integer from 1 to 12."
                )

            check_percent(
                item.get(normal_key),
                f"monthly_vital_statistics.{ticker}.{normal_key}",
            )
            check_percent(
                item.get(midterm_key),
                f"monthly_vital_statistics.{ticker}.{midterm_key}",
            )
            check_page(
                item.get("source_page"),
                f"monthly_vital_statistics.{ticker}.source_page",
            )

            method = str(item.get("extraction_method", "")).lower()
            if "fallback" in method:
                errors.append(
                    f"{ticker} contains a prohibited fallback method."
                )

    # Validate all 11 sectors.
    sector_signals = report.get("sector_signals")

    if not isinstance(sector_signals, dict):
        errors.append("sector_signals must be an object.")
    else:
        actual_sectors = set(sector_signals)

        if actual_sectors != REQUIRED_SECTORS:
            missing = REQUIRED_SECTORS - actual_sectors
            extra = actual_sectors - REQUIRED_SECTORS

            if missing:
                errors.append(
                    f"Missing required sectors: {sorted(missing)}."
                )

            if extra:
                errors.append(
                    f"Unexpected sectors found: {sorted(extra)}."
                )

        for ticker in REQUIRED_SECTORS & actual_sectors:
            item = sector_signals[ticker]

            if item.get("project_ticker") != ticker:
                errors.append(
                    f"{ticker} project_ticker does not match its dictionary key."
                )

            if item.get("signal") not in {"LONG", "SHORT"}:
                errors.append(
                    f"{ticker} signal must be LONG or SHORT."
                )

            for return_key in (
                "average_return_25_year",
                "average_return_10_year",
                "average_return_5_year",
            ):
                check_percent(
                    item.get(return_key),
                    f"sector_signals.{ticker}.{return_key}",
                )

            check_page(
                item.get("source_page"),
                f"sector_signals.{ticker}.source_page",
            )

            method = str(item.get("extraction_method", "")).lower()
            if "fallback" in method:
                errors.append(
                    f"{ticker} contains a prohibited fallback method."
                )

    # Validate weekly evidence.
    weekly_pattern = report.get("week_specific_pattern")

    if not isinstance(weekly_pattern, dict):
        errors.append("week_specific_pattern must be an object.")
    else:
        check_page(
            weekly_pattern.get("source_page"),
            "week_specific_pattern.source_page",
        )

        method = str(
            weekly_pattern.get("extraction_method", "")
        ).lower()

        if "fallback" in method:
            errors.append(
                "Weekly pattern contains a prohibited fallback method."
            )

    if errors:
        raise ValueError(
            "R3 report validation failed:\n- " + "\n- ".join(errors)
        )

    print(
        "R3 validation passed: "
        "3 indices, 11 sectors, valid dates and no invalid values."
    )

def write_beautiful_markdown(path: Path, report: dict[str, Any]) -> None:
    m_lower = TARGET_MONTH.lower()
    m_cap = TARGET_MONTH.capitalize()
    
    md = f"""# {report['agent']} Analysis - {report['week']}
Generated at: `{report['generated_at']}`  
Database Source: `{report['source_file']}`  
Automation Node: `Fully Parameterized Cloud Workflow (T+1 Forecast Roll)`

---

## 📅 Execution Window & Macro Context

| Dimension | Value |
|---|---|
| **Report Generation Week** | {report['week']} |
| **Prediction Target Date Range** | {report['date_range']} |
| **Detected Month Context** | {m_cap} Baseline |
| **Four-Year Cycle Phase** | {report['cycle_context']['cycle']} |

> **Cycle Context Summary:** {report['cycle_context']['summary']}

---

## 📊 {m_cap} Vital Statistics

| Index Asset | Target Index Name | {m_cap} Historical Rank | Expected Average Return | Midterm Year Avg Return | Evidence Page |
|---|---|:---:|:---:|:---:|:---:|
"""
    for ticker, item in report["monthly_vital_statistics"].items():
        rank_val = item.get(f"{m_lower}_rank", "N/A")
        norm_ret = item.get(f"normal_{m_lower}_average_return", "N/A")
        mid_ret = item.get(f"midterm_{m_lower}_average_return", "N/A")
        md += f"| {ticker} | {item['index']} | {rank_val} | {norm_ret} | {mid_ret} | Page {item['source_page']} |\n"

    wp = report["week_specific_pattern"]
    md += f"""
---

## 🧩 Week-Specific Calendar Pattern

**Pattern Descriptor:** {wp['name']}  
**Extraction Method:** `{wp['extraction_method']}`  

> ### 📜 Historical Database Evidence (Page {wp['source_page']})
> {wp['evidence']}

**Operational Interpretation:** {wp['interpretation']}

---

## 📈 Sector Index Seasonality Matrix (Complete 11 GICS Sectors)

| ETF Proxy | Project Target Sector | Historical PDF Ticker | PDF Sector Category | Seasonal Trading Signal | Optimum Calendar Window | 25-Year Avg Return | Evidence Page |
|---|---|---|---|:---:|---|:---:|:---:|
"""
    for ticker, item in report["sector_signals"].items():
        md += (
            f"| **{ticker}** | {item['project_sector']} | {item['pdf_ticker']} | {item['pdf_sector']} | "
            f"`{item['signal']}` | {item['seasonal_window']} | **{item['average_return_25_year']}** | Page {item['source_page']} |\n"
        )

    md += f"""
---

## 🎯 Executive Bias & Tactical Thesis

### ⚖️ Strategic Almanac Bias
**{report['almanac_bias']}**

### 🧠 Operational Confidence
**{report['confidence']}**

### 📝 Quantitative Rationale & Thesis
{report['thesis']}
"""
    path.write_text(md, encoding="utf-8")

def main() -> None:
    folder = script_folder()
    repo_root = folder.parent
    output_dir = repo_root / "outputs" / "R3"
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = find_pdf(folder)
    print(f"Executing parameter-driven forecast run with asset: {pdf_path.name}")

    pages = read_pdf_pages(pdf_path)
    report = build_report(pdf_path, pages)
    validate_report(report)

    # 1. Output structured JSON Matrix 
    # Only begin writing files after validation passes.
    json_path = output_dir / f"almanac_agent_{WEEK}.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False,), encoding="utf-8")

    # 2. Output Data Evidence CSV (Fused Legacy Rich Architecture)
    csv_path = output_dir / f"almanac_agent_{WEEK}.csv"
    m_lower = TARGET_MONTH.lower()
    m_cap = TARGET_MONTH.capitalize()
    
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "ticker", "name", "signal", "window_or_rank", "return_or_evidence", "source_page", "extraction_method"])
        
        for ticker, item in report["monthly_vital_statistics"].items():
            rank_val = item.get(f"{m_lower}_rank", "N/A")
            norm_ret = item.get(f"normal_{m_lower}_average_return", "N/A")
            mid_ret = item.get(f"midterm_{m_lower}_average_return", "N/A")
            composite_evidence = f"Normal {m_cap} {norm_ret}; Midterm {m_cap} {mid_ret}"
            writer.writerow(["index_stat", ticker, item["index"], "", f"{m_cap} rank {rank_val}", composite_evidence, item["source_page"], item["extraction_method"]])
            
        for ticker, item in report["sector_signals"].items():
            writer.writerow(["sector_signal", ticker, item["project_sector"], item["signal"], item["seasonal_window"], item["average_return_25_year"], item["source_page"], item["extraction_method"]])

        wp = report["week_specific_pattern"]
        # Injected DATE_RANGE to guarantee row-level data mutation across rolling forecast weeks
        writer.writerow(["week_pattern", WEEK, wp["name"], "", f"Forecast: {DATE_RANGE}", wp["evidence"], wp["source_page"], wp["extraction_method"]])

    # 3. Output Beautiful Fused Markdown Report
    md_path = output_dir / f"almanac_agent_{WEEK}.md"
    write_beautiful_markdown(md_path, report)

    print(f"Successfully compiled all unified artifacts for execution node: outputs/almanac_agent_{WEEK}.*")

if __name__ == "__main__":
    main()