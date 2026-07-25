import os
import math
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

# ==========================================
# 🛠️ HELPER FUNCTIONS
# ==========================================

def normalize_week(week_str: str) -> str:
    """
    Standardizes week string format to 'WXX' (e.g., '30' -> 'W30', 'w30' -> 'W30').
    """
    if not week_str:
        return ""
    clean_str = str(week_str).strip().upper()
    if not clean_str.startswith("W"):
        clean_str = f"W{clean_str}"
    return clean_str

# ... (Retain existing imports, ASSETS, and CORE_ASSETS definitions) ...

def number(value, missing="N/A"):
    """Format numbers for Markdown. Strictly blocks non-finite values to prevent silent data corruption."""
    if value is None:
        return missing
    # Intercept NaN/Inf during string formatting to fail fast
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"CRITICAL: Encountered non-finite number during Markdown formatting: {value}")
    return f"{float(value):,.2f}" if isinstance(value, (int, float)) else str(value)


def write_markdown(snapshot: dict, path: Path):
    metrics = snapshot["metrics"]
    week = snapshot["meta"]["market_week"]
    lines = [f"# R5 Technical Agent Report: {week}", "", "## Cross-Asset Technical Matrix", "",
             "| Asset | Close | EMA 8 | EMA 21 | Support | Resistance | Trend | Bias | Confidence |",
             "|---|---:|---:|---:|---:|---:|---|---|---|"]
    for label in ASSETS:
        if label not in metrics:
            continue
        item = metrics[label]
        lines.append(
            f"| {label} | {number(item['close_price'])} | {number(item['ema_8'])} | "
            f"{number(item['ema_21'])} | {number(item['support'])} | {number(item['resistance'])} | "
            f"{item['trend']} | {item['bias']} | {item['confidence']} |"
        )
    for label in ASSETS:
        if label not in metrics:
            continue
        item = metrics[label]
        lines += ["", f"## {item['asset_name']} ({label})", "", f"![{label} chart]({item['chart_file']})", "",
                  f"- **Close price:** {number(item['close_price'])}", f"- **EMA 8:** {number(item['ema_8'])}",
                  f"- **EMA 21:** {number(item['ema_21'])}", f"- **Support:** {number(item['support'])}",
                  f"- **Resistance:** {number(item['resistance'], 'No clear nearby resistance')}",
                  f"- **Trend:** {item['trend']}", f"- **Bias:** {item['bias']}",
                  f"- **Confidence:** {item['confidence']}"]
    lines += ["", "## Methodology Note", "",
              "The JSON writer rejects NaN and infinity. Invalid core prices cause the workflow to fail instead of publishing incorrect values.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_all_metrics(metrics: dict):
    """Deep scan all metrics to find root causes of calculation issues (e.g., NaN/Inf in any field)."""
    errors = []
    for label, item in metrics.items():
        if not isinstance(item, dict):
            errors.append(f"{label} is not a dictionary")
            continue
        for key, value in item.items():
            # Check all numeric fields for non-finite values
            if isinstance(value, float) and not math.isfinite(value):
                errors.append(f"{label}.{key} is non-finite ({value})")
    
    if errors:
        # Raise detailed error to help identify the root cause in CI logs
        raise RuntimeError("Metrics validation failed (Non-finite values detected):\n - " + "\n - ".join(errors))


def validate_core(snapshot: dict):
    """First line of defense: ensure core assets exist and critical fields are strictly valid."""
    errors = []
    for label in CORE_ASSETS:
        item = snapshot["metrics"].get(label)
        if not item:
            errors.append(f"Core asset {label} is missing from metrics")
            continue
        for field in ("close_price", "ema_8", "ema_21"):
            value = item.get(field)
            if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                errors.append(f"Core asset {label}.{field} is invalid or non-finite: {value!r}")
    if errors:
        raise RuntimeError("Core validation failed:\n - " + "\n - ".join(errors))


def run(week: str, year: int, output_dir: Path):
    week = normalize_week(week)
    start, end, final_date = trading_window(week, year)
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_dir = output_dir / "charts" / week
    
    snapshot = {
        "meta": {
            "agent": "R5 Technical Agent",
            "market_week": week,
            "market_year": year,
            "generation_time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "data_source": "Yahoo Finance via yfinance",
            "data_window_start": start,
            "data_window_end": final_date,
            "requested_asset_count": len(ASSETS),
            "successful_asset_count": 0,
            "failed_asset_count": 0,
        },
        "metrics": {},
        "errors": {},
    }
    
    for label, (symbol, name) in ASSETS.items():
        try:
            snapshot["metrics"][label] = analyze(label, symbol, name, start, end, week, chart_dir)
        except Exception as exc:
            # Log detailed root cause to stderr and snapshot errors for debugging
            snapshot["errors"][label] = f"{type(exc).__name__}: {exc}"
            print(f"ERROR [{label}]: {exc}", file=sys.stderr)
            
    snapshot["meta"]["successful_asset_count"] = len(snapshot["metrics"])
    snapshot["meta"]["failed_asset_count"] = len(snapshot["errors"])
    
    # Execute two-phase validation before writing any files
    validate_core(snapshot)
    validate_all_metrics(snapshot["metrics"])

    json_path = output_dir / f"technical_agent_{week}.json"
    md_path = output_dir / f"technical_agent-{week}.md"
    
    # allow_nan=False is the final safeguard to prevent NaN serialization
    json_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    write_markdown(snapshot, md_path)
    
    print(f"Successfully generated: {json_path}")
    print(f"Successfully generated: {md_path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--market-week", required=True)
    parser.add_argument("--year", type=int, default=datetime.now(timezone.utc).year)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()
    try:
        run(args.market_week, args.year, Path(args.output_dir))
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
