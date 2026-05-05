"""Fetch a snapshot of all NSE F&O tickers from Yahoo Finance and write snapshot.json.

Output schema:
  {
    "fetched_at": "<UTC ISO>",
    "source": "...",
    "trading_days": ["YYYY-MM-DD", ...  ~252 entries],
    "rows": [
      {"s": "RELIANCE", "p": 1339.0, "d1": ..., "w1": ..., "m1": ..., "y1": ...,
       "h": ..., "m": <mcap_cr>, "c": [<close per trading_day>, null if missing]},
      ...
    ]
  }

The trading_days array is shared; per-ticker `c` array is parallel to it.
The dashboard uses this for arbitrary date-range return calculations.

Usage:  python scripts/fetch_fno_snapshot.py
"""
import json, sys, datetime as dt
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request, urllib.error

import yfinance as yf
import pandas as pd

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
OUT_FILE = REPO_ROOT / "snapshot.json"

NSE_URL = "https://www.nseindia.com/api/underlying-information"
NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

HISTORY_DAYS = 1260   # ~5 years of trading days


def get_fno_symbols():
    try:
        req = urllib.request.Request(NSE_URL, headers=NSE_HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        symbols = sorted({row["symbol"] for row in data["data"]["UnderlyingList"]})
        if not symbols:
            raise ValueError("Empty UnderlyingList from NSE")
        print(f"Fetched {len(symbols)} F&O symbols live from NSE.", file=sys.stderr)
        return symbols
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"NSE fetch failed ({e}); falling back to scripts/fno_tickers.py", file=sys.stderr)
        sys.path.insert(0, str(SCRIPT_DIR))
        from fno_tickers import FNO_TICKERS
        return list(FNO_TICKERS)


def pct(curr, ref):
    if curr is None or ref is None or ref == 0:
        return None
    try:
        return round((curr / ref - 1.0) * 100.0, 2)
    except Exception:
        return None


def fetch_prices_and_returns(yf_symbols):
    print(f"Downloading {len(yf_symbols)} tickers (with daily history)...", file=sys.stderr)
    data = yf.download(
        yf_symbols, period="5y", interval="1d",
        group_by="ticker", auto_adjust=False, progress=False, threads=True,
    )

    today = pd.Timestamp.utcnow().tz_localize(None).normalize()
    target_1w = today - pd.Timedelta(days=7)
    target_1m = today - pd.DateOffset(months=1)
    target_1y = today - pd.DateOffset(years=1)

    rows = []
    for sym in yf_symbols:
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
        close = close.iloc[-HISTORY_DAYS:]

        last_price = float(close.iloc[-1])
        prev_close = float(close.iloc[-2]) if len(close) >= 2 else None

        def ref_price(target):
            pos = close.index.searchsorted(target, side="right") - 1
            return float(close.iloc[pos]) if pos >= 0 else None

        rows.append({
            "s": sym.replace(".NS", ""),
            "p": round(last_price, 2),
            "d1": pct(last_price, prev_close),
            "w1": pct(last_price, ref_price(target_1w)),
            "m1": pct(last_price, ref_price(target_1m)),
            "y1": pct(last_price, ref_price(target_1y)),
            "h":  pct(last_price, float(close.max())),
            "_dates":  [d.strftime("%Y-%m-%d") for d in close.index],
            "_closes": [round(float(v), 2) for v in close.values],
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
                by_sym[sym]["m"] = round(mcap / 1e7, 0) if mcap else None


def align_to_canonical_dates(rows):
    """Build a canonical trading_days array (longest history) and align each
    ticker's closes to it (insert null where the ticker has no data)."""
    canonical_dates = max((r["_dates"] for r in rows), key=len, default=[])
    date_index = {d: i for i, d in enumerate(canonical_dates)}
    n = len(canonical_dates)
    out_rows = []
    for r in rows:
        closes = [None] * n
        for d, c in zip(r["_dates"], r["_closes"]):
            idx = date_index.get(d)
            if idx is not None:
                closes[idx] = c
        out = {k: v for k, v in r.items() if not k.startswith("_")}
        out["c"] = closes
        out_rows.append(out)
    return canonical_dates, out_rows


def main():
    symbols = get_fno_symbols()
    yf_symbols = [s + ".NS" for s in symbols]

    rows = fetch_prices_and_returns(yf_symbols)
    fetch_market_caps(rows)
    canonical_dates, rows_out = align_to_canonical_dates(rows)

    out = {
        "fetched_at": dt.datetime.utcnow().isoformat() + "Z",
        "source": "NSE underlying-information API + Yahoo Finance",
        "trading_days": canonical_dates,
        "rows": rows_out,
    }
    OUT_FILE.write_text(json.dumps(out, separators=(",", ":")))
    print(f"Wrote {OUT_FILE} with {len(rows_out)} rows × {len(canonical_dates)} trading days.", file=sys.stderr)


if __name__ == "__main__":
    main()
