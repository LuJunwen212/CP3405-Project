import os
import math
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# ==========================================
# 🌐 GLOBAL CONSTANTS & ASSET DEFINITIONS
# ==========================================

ASSETS = {
    "SPX": ("^GSPC", "S&P 500 Index"),
    "NDX": ("^NDX", "Nasdaq 100 Index"),
    "IWM": ("IWM", "iShares Russell 2000 ETF"),
    "XLC": ("XLC", "Communication Services Select Sector SPDR Fund"),
    "XLY": ("XLY", "Consumer Discretionary Select Sector SPDR Fund"),
    "XLP": ("XLP", "Consumer Staples Select Sector SPDR Fund"),
    "XLE": ("XLE", "Energy Select Sector SPDR Fund"),
    "XLF": ("XLF", "Financial Select Sector SPDR Fund"),
    "XLV": ("XLV", "Health Care Select Sector SPDR Fund"),
    "XLI": ("XLI", "Industrial Select Sector SPDR Fund"),
    "XLB": ("XLB", "Materials Select Sector SPDR Fund"),
    "XLRE": ("XLRE", "Real Estate Select Sector SPDR Fund"),
    "XLK": ("XLK", "Technology Select Sector SPDR Fund"),
    "XLU": ("XLU", "Utilities Select Sector SPDR Fund")
}

CORE_ASSETS = ["SPX", "NDX", "IWM"]

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


def trading_window(week_str: str, year: int):
    """
    Calculates date range for data fetching based on ISO week number and year.
    Returns: (start_date, end_date, final_date)
    """
    clean_week = normalize_week(week_str).replace("W", "")
    week_num = int(clean_week)
    
    monday = datetime.strptime(f"{year}-W{week_num:02d}-1", "%G-W%V-%u").date()
    friday = monday + timedelta(days=4)
    saturday = monday + timedelta(days=5)
    
    start_date = (monday - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = saturday.strftime("%Y-%m-%d")
    final_date = friday.strftime("%Y-%m-%d")
    
    return start_date, end_date, final_date


def number(value, missing="N/A"):
    """
    Formats numbers for Markdown output. Strictly blocks non-finite values (NaN/Inf).
    """
    if value is None:
        return missing
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"CRITICAL: Encountered non-finite number during Markdown formatting: {value}")
    return f"{float(value):,.2f}" if isinstance(value, (int, float)) else str(value)

# ==========================================
# 📈 CHART GENERATION
# ==========================================

def generate_chart(df: pd.DataFrame, label: str, name: str, output_file: Path, start_date: str, end_date: str):
    """
    Generates candlestick chart with EMA 8, EMA 21, Volume, and custom headers.
    Saves image using pattern: chart_{ASSET}_{WEEK}.png
    """
    try:
        plot_df = df.tail(120).copy()

        # Compute exponential moving averages for chart overlay
        plot_df['EMA8'] = plot_df['Close'].ewm(span=8, adjust=False).mean()
        plot_df['EMA21'] = plot_df['Close'].ewm(span=21, adjust=False).mean()

        add_plots = [
            mpf.makeaddplot(plot_df['EMA8'], color='#ff7f0e', width=1.2),  # Orange line
            mpf.makeaddplot(plot_df['EMA21'], color='#1f77b4', width=1.2)  # Blue line
        ]

        title_text = f"{label} - {name}\nDate: {start_date} to {end_date}"

        # Clean high-contrast chart styling
        style = mpf.make_mpf_style(
            base_mpf_style='nightclouds',
            rc={
                'font.size': 9,
                'axes.titlesize': 10,
                'figure.titlesize': 11
            }
        )

        output_file.parent.mkdir(parents=True, exist_ok=True)

        mpf.plot(
            plot_df,
            type='candle',
            style=style,
            addplot=add_plots,
            volume=True,
            title=title_text,
            savefig=dict(fname=str(output_file), dpi=150, bbox_inches='tight'),
            figscale=1.1
        )
        print(f"📈 Chart successfully generated: {output_file.name}")
    except Exception as e:
        print(f"⚠️ Failed to generate chart for [{label}]: {e}", file=sys.stderr)

# ==========================================
# 📊 TECHNICAL CALCULATIONS
# ==========================================

def calculate_indicators(df: pd.DataFrame):
    """
    Calculates technical metrics: Close, EMA 8, EMA 21, RSI 14, Support, and Resistance.
    """
    if df.empty or len(df) < 21:
        raise ValueError("Insufficient price data retrieved to compute technical indicators.")

    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    last_close = float(close.iloc[-1])
    ema_8 = float(close.ewm(span=8, adjust=False).mean().iloc[-1])
    ema_21 = float(close.ewm(span=21, adjust=False).mean().iloc[-1])

    # RSI Calculation (14 periods)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    last_rsi = float(rsi_series.iloc[-1]) if math.isfinite(rsi_series.iloc[-1]) else 50.0

    # Rolling Support and Resistance (52-week min/max)
    support = float(close.tail(252).min())
    resistance = float(close.tail(252).max())

    # Trend and Bias classification
    if last_close > ema_8 and ema_8 > ema_21:
        trend = "Bullish"
        bias = "Bullish"
    elif last_close < ema_8 and ema_8 < ema_21:
        trend = "Bearish"
        bias = "Bearish"
    else:
        trend = "Neutral"
        bias = "Neutral"

    return {
        "close_price": last_close,
        "ema_8": ema_8,
        "ema_21": ema_21,
        "rsi": last_rsi,
        "support": support,
        "resistance": resistance,
        "trend": trend,
        "bias": bias,
        "confidence": "Medium"
    }


def validate_core(snapshot: dict):
    """
    Ensures all core assets are present in metrics snapshot.
    """
    missing = [core for core in CORE_ASSETS if core not in snapshot["metrics"]]
    if missing:
        raise RuntimeError(f"Core validation failed: The following core assets are missing from metrics: {missing}")


def validate_all_metrics(metrics: dict):
    """
    Recursively validates that all numerical values are finite numbers.
    """
    for asset_name, item in metrics.items():
        if isinstance(item, dict):
            for key, val in item.items():
                if isinstance(val, float) and not math.isfinite(val):
                    raise ValueError(f"Validation Error: Non-finite value in {asset_name}.{key}: {val}")


def write_markdown(snapshot: dict, path: Path):
    """
    Generates structured Markdown report for R5 Technical Agent output.
    """
    metrics = snapshot["metrics"]
    week = snapshot["meta"]["market_week"]
    lines = [
        f"# R5 Technical Agent Report: {week}", "",
        "## Cross-Asset Technical Matrix", "",
        "| Asset | Close | EMA 8 | EMA 21 | Support | Resistance | Trend | Bias | Confidence |",
        "|---|---:|---:|---:|---:|---:|---|---|---|"
    ]
    for label in ASSETS:
        if label not in metrics:
            continue
        item = metrics[label]
        lines.append(
            f"| {label} | {number(item['close_price'])} | {number(item['ema_8'])} | "
            f"{number(item['ema_21'])} | {number(item['support'])} | {number(item['resistance'])} | "
            f"{item['trend']} | {item['bias']} | {item['confidence']} |"
        )
    
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

# ==========================================
# 🚀 PIPELINE EXECUTION
# ==========================================

def run(week_str: str, year: int, output_dir: Path):
    """
    Executes technical analysis pipeline, validations, and exports output files.
    """
    week = normalize_week(week_str)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    chart_dir = output_dir / "charts" / week
    chart_dir.mkdir(parents=True, exist_ok=True)

    start_date, end_date, final_date = trading_window(week, year)

    print(f"📊 Running R5 Technical Pipeline for {week} ({year}) | Date Range: {start_date} to {end_date}")

    snapshot = {
        "meta": {
            "market_week": week,
            "year": year,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data_start": start_date,
            "data_end": end_date,
            "final_trading_day": final_date
        },
        "metrics": {},
        "errors": {}
    }

    for label, (symbol, name) in ASSETS.items():
        try:
            df = yf.download(symbol, start=start_date, end=end_date, progress=False)
            if df.empty:
                raise ValueError(f"No price data retrieved for {symbol} ({name})")

            # Resolve multi-level column indexing if present in recent yfinance releases
            if isinstance(df.columns, pd.MultiIndex):
                if 'Ticker' in df.columns.names:
                    df = df.xs(symbol, level='Ticker', axis=1)
                else:
                    df = df.droplevel(1, axis=1)

            snapshot["metrics"][label] = calculate_indicators(df)
            
            # Save chart following required filename format: chart_{ASSET}_{WEEK}.png
            chart_file = chart_dir / f"chart_{label}_{week}.png"
            generate_chart(df, label, name, chart_file, start_date, end_date)

            print(f"✅ [{label}] Technical analysis successfully compiled.")
        except Exception as exc:
            snapshot["errors"][label] = f"{type(exc).__name__}: {exc}"
            print(f"ERROR [{label}]: {exc}", file=sys.stderr)

    snapshot["meta"]["successful_asset_count"] = len(snapshot["metrics"])
    snapshot["meta"]["failed_asset_count"] = len(snapshot["errors"])

    # Strict validations before file serialization
    validate_core(snapshot)
    validate_all_metrics(snapshot["metrics"])

    json_path = output_dir / f"technical_agent_{week}.json"
    md_path = output_dir / f"technical_agent-{week}.md"

    json_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    write_markdown(snapshot, md_path)

    print(f"Successfully generated: {json_path}")
    print(f"Successfully generated: {md_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="R5 Technical Analysis Automation Tool")
    parser.add_argument("--market-week", required=True, help="Target market week (e.g., W30)")
    parser.add_argument("--year", type=int, default=datetime.now(timezone.utc).year)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    try:
        run(args.market_week, args.year, Path(args.output_dir))
        return 0
    except Exception as e:
        print(f"FATAL: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
