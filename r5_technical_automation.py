#!/usr/bin/env python3
"""R5 Technical Agent: generate strict JSON, Markdown, and market charts."""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import mplfinance as mpf
import pandas as pd
import yfinance as yf

HISTORY_DAYS = 365
CHART_DAYS = 15
CORE_ASSETS = ("SPX", "NDX", "IWM")
ASSETS = {
    "SPX": ("^GSPC", "S&P 500"),
    "NDX": ("^NDX", "NASDAQ 100"),
    "IWM": ("IWM", "Russell 2000 ETF"),
    "XLK": ("XLK", "Technology"),
    "XLU": ("XLU", "Utilities"),
    "XLF": ("XLF", "Financials"),
    "XLE": ("XLE", "Energy"),
    "XLB": ("XLB", "Materials"),
    "XLY": ("XLY", "Consumer Discretionary"),
    "XLP": ("XLP", "Consumer Staples"),
    "XLV": ("XLV", "Health Care"),
    "XLI": ("XLI", "Industrials"),
    "XLC": ("XLC", "Communication Services"),
    "XLRE": ("XLRE", "Real Estate"),
}


def normalize_week(value: str) -> str:
    value = value.strip().upper()
    if not value.startswith("W"):
        value = f"W{value}"
    try:
        number = int(value[1:])
    except ValueError as exc:
        raise ValueError("Market week must look like W29 or 29.") from exc
    if not 1 <= number <= 53:
        raise ValueError("Market week must be between W01 and W53.")
    return f"W{number:02d}"


def trading_window(market_week: str, year: int) -> tuple[str, str, str]:
    week_number = int(normalize_week(market_week)[1:])
    monday = datetime.fromisocalendar(year, week_number, 1)
    friday = monday + timedelta(days=4)
    start = (monday - timedelta(days=HISTORY_DAYS)).strftime("%Y-%m-%d")
    end_exclusive = (friday + timedelta(days=1)).strftime("%Y-%m-%d")
    return start, end_exclusive, friday.strftime("%Y-%m-%d")


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        prices = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}
        level0 = set(map(str, df.columns.get_level_values(0)))
        level1 = set(map(str, df.columns.get_level_values(1)))
        if prices & level0:
            df.columns = df.columns.get_level_values(0)
        elif prices & level1:
            df.columns = df.columns.get_level_values(1)
        else:
            df.columns = ["_".join(map(str, col)) for col in df.columns]
    return df.loc[:, ~df.columns.duplicated()].copy()


def finite(value: Any, name: str) -> float:
    if isinstance(value, pd.Series):
        if len(value) != 1:
            raise ValueError(f"{name} contains multiple values")
        value = value.iloc[0]
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} is invalid: {number}")
    return number


def download(symbol: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(
        symbol,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        progress=False,
        threads=False,
        group_by="column",
    )
    if df.empty:
        raise RuntimeError(f"No Yahoo Finance data returned for {symbol}")
    df = flatten_columns(df)
    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise RuntimeError(f"{symbol} missing columns: {missing}")
    for column in required:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.replace([math.inf, -math.inf], pd.NA)
    df = df.dropna(subset=["Open", "High", "Low", "Close"]).copy()
    if df.empty:
        raise RuntimeError(f"{symbol} has no valid OHLC rows")
    df["Volume"] = df["Volume"].fillna(0.0)
    return df


def support_resistance(df: pd.DataFrame, lookback: int = 60, window: int = 3):
    recent = df.tail(lookback)
    close = finite(recent["Close"].iloc[-1], "close")
    lows, highs = [], []
    for i in range(window, len(recent) - window):
        low = finite(recent["Low"].iloc[i], "pivot low")
        high = finite(recent["High"].iloc[i], "pivot high")
        if low == finite(recent["Low"].iloc[i-window:i+window+1].min(), "window low"):
            lows.append(low)
        if high == finite(recent["High"].iloc[i-window:i+window+1].max(), "window high"):
            highs.append(high)
    supports = [value for value in lows if value < close]
    resistances = [value for value in highs if value > close]
    support = max(supports) if supports else finite(recent["Low"].min(), "support")
    resistance = min(resistances) if resistances else None
    return round(support, 4), round(resistance, 4) if resistance is not None else None


def classify(close: float, ema8: float, ema21: float):
    if close > ema8 > ema21:
        return "Bullish / Recovery", "Bullish", "Medium"
    if close < ema8 < ema21:
        return "Bearish", "Bearish", "Medium"
    if close > ema8 and ema8 < ema21:
        return "Mixed / Early Recovery", "Slightly Bullish", "Low"
    if close < ema8 and ema8 > ema21:
        return "Pullback / Weakening", "Slightly Bearish", "Low"
    return "Neutral / Mixed", "Neutral", "Low"


def create_chart(df: pd.DataFrame, label: str, week: str, chart_dir: Path) -> Path:
    chart_dir.mkdir(parents=True, exist_ok=True)
    data = df.tail(CHART_DAYS).copy()
    path = chart_dir / f"chart_{label}_{week}.png"
    style = mpf.make_mpf_style(base_mpf_style="yahoo", rc={"axes.edgecolor": "black"})
    plots = [
        mpf.make_addplot(data["EMA_8"], color="#ec915c", width=2, label="EMA 8"),
        mpf.make_addplot(data["EMA_21"], color="#4687d3", width=2, label="EMA 21"),
    ]
    mpf.plot(
        data,
        type="candle",
        style=style,
        volume=True,
        addplot=plots,
        title=f"{label} - {week}\nGenerated on {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S UTC}",
        ylabel="Price",
        ylabel_lower="Volume",
        tight_layout=True,
        savefig={"fname": str(path), "dpi": 140, "pad_inches": 0.5},
    )
    return path


def analyze(label: str, symbol: str, name: str, start: str, end: str, week: str, chart_dir: Path):
    print(f"Processing {label} ({symbol})")
    df = download(symbol, start, end)
    df["EMA_8"] = df["Close"].ewm(span=8, adjust=False).mean()
    df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()
    close = finite(df["Close"].iloc[-1], f"{label} close")
    ema8 = finite(df["EMA_8"].iloc[-1], f"{label} EMA 8")
    ema21 = finite(df["EMA_21"].iloc[-1], f"{label} EMA 21")
    support, resistance = support_resistance(df)
    trend, bias, confidence = classify(close, ema8, ema21)
    chart = create_chart(df, label, week, chart_dir)
    return {
        "ticker": symbol,
        "asset_name": name,
        "last_trading_date": df.index[-1].strftime("%Y-%m-%d"),
        "close_price": round(close, 4),
        "ema_8": round(ema8, 4),
        "ema_21": round(ema21, 4),
        "support": support,
        "resistance": resistance,
        "trend": trend,
        "bias": bias,
        "confidence": confidence,
        "chart_file": chart.as_posix(),
        "data_rows": int(len(df)),
    }


def number(value, missing="N/A"):
    if value is None:
        return missing
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


def validate_core(snapshot: dict):
    errors = []
    for label in CORE_ASSETS:
        item = snapshot["metrics"].get(label)
        if not item:
            errors.append(f"{label} missing")
            continue
        for field in ("close_price", "ema_8", "ema_21"):
            value = item.get(field)
            if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                errors.append(f"{label}.{field}={value!r}")
    if errors:
        raise RuntimeError("Core validation failed: " + "; ".join(errors))


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
            snapshot["errors"][label] = f"{type(exc).__name__}: {exc}"
            print(f"ERROR {label}: {exc}", file=sys.stderr)
    snapshot["meta"]["successful_asset_count"] = len(snapshot["metrics"])
    snapshot["meta"]["failed_asset_count"] = len(snapshot["errors"])
    validate_core(snapshot)
    json_path = output_dir / f"technical_agent_{week}.json"
    md_path = output_dir / f"technical_agent-{week}.md"
    json_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    write_markdown(snapshot, md_path)
    print(f"Generated: {json_path}")
    print(f"Generated: {md_path}")


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
