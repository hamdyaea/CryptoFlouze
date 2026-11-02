# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
import unittest
from CryptoFlouze import parse_tickers

class MarketTests(unittest.TestCase):
    def test_parse_and_sort(self):
        data = [
            {"rank": 2, "name": "Coin B", "quotes": {"USD": {"price": 5.2}}},
            {"rank": 1, "name": "Coin A", "quotes": {"USD": {"price": 2.5}}},
            {"rank": None, "name": "Unknown", "quotes": {}},
        ]
        self.assertEqual(parse_tickers(data, 1), [(1, "Coin A", 2.5)])
    def test_invalid_payload(self):
        with self.assertRaises(ValueError):
            parse_tickers({})
    def test_empty(self):
        self.assertEqual(parse_tickers([]), [])

if __name__ == "__main__":
    unittest.main()
