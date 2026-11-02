# CryptoFlouze — Cryptocurrency Market Snapshot

**Developer:** Hamdy Abou El Anein  
**Contact:** info@daylightlinux.ch  
**License:** GPL v3 (see LICENSE).

A Python 3/Tkinter market viewer using the public CoinPaprika API. It replaces EasyGUI, removes the hardcoded CoinMarketCap API key placeholder and uses a background thread to keep the GUI responsive. No API key or third-party Python package is needed.

```sh
python3 CryptoFlouze.py
python3 CryptoFlouze.py --text --limit 10
python3 -m unittest discover -s tests -v
```

The app makes HTTPS requests to CoinPaprika. Live price availability, API limits, freshness and completeness depend on the external provider. Prices are informational, not financial advice.

Original implementation: [old branch](https://github.com/hamdyaea/CryptoFlouze/tree/old).
