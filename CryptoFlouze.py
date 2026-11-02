#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
"""CryptoFlouze: read-only cryptocurrency prices from CoinPaprika."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import tkinter as tk
from tkinter import ttk
from urllib.request import Request, urlopen

BASE = "https://api.coinpaprika.com/v1"
executor = ThreadPoolExecutor(max_workers=1)

def fetch_json(url: str):
    request = Request(url, headers={"User-Agent": "CryptoFlouze/2.0"})
    with urlopen(request, timeout=12) as response:
        payload = response.read(8_000_001)
    if len(payload) > 8_000_000:
        raise ValueError("API response too large")
    return json.loads(payload)

def parse_tickers(data: list[dict], limit: int = 20) -> list[tuple[int, str, float]]:
    if not isinstance(data, list):
        raise ValueError("Expected a list of tickers")
    rows = []
    for item in data:
        if not isinstance(item, dict):
            continue
        rank = item.get("rank")
        quote = item.get("quotes", {}).get("USD", {}) if isinstance(item.get("quotes"), dict) else {}
        price = quote.get("price") if isinstance(quote, dict) else None
        if isinstance(rank, int) and rank > 0 and isinstance(price, (int, float)) and price >= 0:
            rows.append((rank, str(item.get("name", "")), float(price)))
    return sorted(rows)[:limit]

def market_snapshot(limit: int = 20) -> str:
    global_data = fetch_json(BASE + "/global")
    tickers = fetch_json(BASE + "/tickers?quotes=USD")
    cap = global_data.get("market_cap_usd") if isinstance(global_data, dict) else None
    lines = [f"Global market cap: ${cap:,.0f}" if isinstance(cap, (int, float)) else "Global market cap unavailable", "",
             "Rank  Name                         Price (USD)"]
    for rank, name, price in parse_tickers(tickers, limit):
        lines.append(f"{rank:>4}  {name[:28]:<28} ${price:,.6f}")
    lines.append("\nData: CoinPaprika API. Prices may be delayed.")
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", action="store_true", help="Print prices in terminal")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    if args.text:
        try:
            print(market_snapshot(args.limit))
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
        return
    root = tk.Tk()
    root.title("CryptoFlouze — Market Snapshot")
    root.geometry("680x600")
    frame = ttk.Frame(root, padding=15)
    frame.pack(fill="both", expand=True)
    status = tk.StringVar(value="Ready")
    ttk.Label(frame, textvariable=status).pack(anchor="w")
    output = tk.Text(frame, font=("monospace", 11), wrap="none")
    output.pack(fill="both", expand=True, pady=8)
    button = ttk.Button(frame, text="Refresh")
    button.pack()
    def refresh() -> None:
        button.config(state="disabled")
        status.set("Fetching market data…")
        future = executor.submit(market_snapshot, args.limit)
        def poll() -> None:
            if not root.winfo_exists():
                return
            if not future.done():
                root.after(100, poll)
                return
            try:
                text = future.result()
                status.set("Updated")
            except Exception as exc:
                text = f"Could not retrieve market data: {exc}"
                status.set("Unavailable")
            output.delete("1.0", "end")
            output.insert("1.0", text)
            button.config(state="normal")
        root.after(100, poll)
    button.configure(command=refresh)
    refresh()
    root.mainloop()

if __name__ == "__main__":
    main()
