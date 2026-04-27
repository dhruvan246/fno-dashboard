"""Fetch a snapshot of all NSE F&O tickers from Yahoo Finance and write snapshot.json.

Usage:  python scripts/fetch_fno_snapshot.py
Writes: snapshot.json at repo root (one level up from scripts/).
"""
import json
import sys
import datetime as dt
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import yfinance as yf
import pandas as pd

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from fno_tickers import FNO_TICKERS

REPO_ROOT = SCRIPT_DIR.parent
OUT_FILE = REPO_ROOT / "snapshot.json"

YF_SYMBOLS = [t + ".NS" for t in FNO_TICKERS]


def pct(curr, ref):
    if curr is None or ref is None or ref == 0:
        return None
    try:
        return round((curr / ref - 1.0) * 100.0, 2)
    except Exception:
        return None


def nearest_idx_at_or_before(index, target):
    pos = index.searchsorted(target, side="right") - 1
    return int(pos) if pos >= 0 else None


def fetch_prices_and_returns():
    print(f"Downloading {len(YF_SYMBOLS)} tickers in one batch...", file=sys.stderr)
    data = yf.download(
        YF_SYMBOLS,
        period="14mo",
        interval="1d",
        group_by="ticker",
        auto_adjust=False,
        progress=False,
        threads=True,
    )

    today = pd.Timestamp.utcnow().tz_localize(None).normalize()
    target_1w = today - pd.Timedelta(days=7)
    target_1m = today - pd.DateOffset(months=1)
    target_1y = today - pd.DateOffset(years=1)

    rows = []
    for sym in YF_SYMBOLS:
        try:
            df = data[sym].dropna(how="all")
        except KeyError:
            continue
        if df.empty:
            continue
        close = df["Close"].dropna()
        if close.empty:
            continue
        if close.index.tz is not None:
            close.index = close.index.tz_localize(None)

        last_price = float(close.iloc[-1])
        prev_close = float(close.iloc[-2]) if len(close) >= 2 else None

        def ref_price(target):
            pos = nearest_idx_at_or_before(close.index, target)
            return float(close.iloc[pos]) if pos is not None else None

        last_252 = close.iloc[-252:]
        hi_52w = float(last_252.max())

        rows.append({
            "s": sym.replace(".NS", ""),
            "p": round(last_price, 2),
            "d1": pct(last_price, prev_close),
            "w1": pct(last_price, ref_price(target_1w)),
            "m1": pct(last_price, ref_price(target_1m)),
            "y1": pct(last_price, ref_price(target_1y)),
            "h": pct(last_price, hi_52w),
        })
    return rows


def fetch_market_caps(rows):
    print(f"Fetching market caps for {len(rows)} tickers...", file=sys.stderr)

    def get_mcap(sym):
        try:
            return sym, yf.Ticker(sym + ".NS").fast_info.market_cap
        except Exception:
            return sym, None

    by_sym = {r["s"]: r for r in rows}
    with ThreadPoolExecutor(max_workers=30) as ex:
        for fut in as_completed([ex.submit(get_mcap, r["s"]) for r in rows]):
            sym, mcap = fut.result()
            if sym in by_sym:
                # store in crores (1 cr = 1e7), rounded
                by_sym[sym]["m"] = round(mcap / 1e7, 0) if mcap else None


def main():
    rows = fetch_prices_and_returns()
    fetch_market_caps(rows)
    out = {
        "fetched_at": dt.datetime.utcnow().isoformat() + "Z",
        "rows": rows,
    }
    OUT_FILE.write_text(json.dumps(out, separators=(",", ":")))
    print(f"Wrote {OUT_FILE} with {len(rows)} rows.", file=sys.stderr)


if __name__ == "__main__":
    main()
