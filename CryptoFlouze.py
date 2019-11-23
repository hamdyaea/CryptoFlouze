#!/usr/bin/env python3

"""
Developer : Hamdy Abou El Anein
https://github.com/hamdyaea
hamdy.aea@protonmail.com
"""

# You need to have an free  API key from https://coinmarketcap.com/api/ You have to put it on line 70.

from requests import Session
import json
from easygui import *
import sys
import urllib.request


class Crypto:
    def __init__(self):
        self.image
        self.choices
        self.reply
        self.data
        self.data_start
        self.coin
        self.a
        self.b
        self.c
        self.msg
        self.global_market
        self.global_market_cap
        self.url


def start():
    main()
    gui()


def gui():
    Crypto.image = "./Pictures/crypto.jpg"
    Crypto.choices = ["Reload"]
    Crypto.reply = buttonbox(Crypto.msg, image=Crypto.image, choices=Crypto.choices)
    if Crypto.reply == "Reload":
        start()
    elif Crypto.reply == "./Pictures/crypto.jpg":
        start()
    else:
        sys.exit(0)


def main():
    try:
        urlData = "https://api.coinpaprika.com/v1/global"
        webURL = urllib.request.urlopen(urlData)
        Crypto.data = webURL.read()
        encoding = webURL.info().get_content_charset("utf-8")
        Crypto.global_market = json.loads(Crypto.data.decode(encoding))
        Crypto.global_market_cap = Crypto.global_market["market_cap_usd"]
        Crypto.url = (
            "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        )
        parameters = {
            "start": "1",
            "limit": "20",
            "convert": "USD",
        }
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "XXXXXX-XXXX-XXXX-XXXXX-XXXXXX",  # Enter your https://coinmarketcap.com/api/  api key  here
        }
        session = Session()
        session.headers.update(headers)
        response = session.get(Crypto.url, params=parameters)
        Crypto.data = json.loads(response.text)
        Crypto.data_start = Crypto.data["data"]
        Crypto.coin = ""
        for i in Crypto.data_start:
            Crypto.a = str(i["cmc_rank"])  # Rank
            Crypto.b = str(i["name"])  # Name
            Crypto.c = str(i["quote"]["USD"]["price"])  # Price
            Crypto.coin = (
                Crypto.coin
                + ((Crypto.a) + ("{: ^20}".format(Crypto.b)) + (Crypto.c))
                + str(" $")
                + str("\n")
            )
        Crypto.msg = (
            ("                    CryptoFlouze")
            + str("\n\n               Global Crypto Market Cap   ")
            + str(Crypto.global_market_cap)
            + str(" $")
            + str("\n\n")
            + str(Crypto.coin)
            + str("\nAll prices are in USD and updated at every run of this software")
            + str("\n\nDeveloper : Hamdy Abou El Anein\nhttps://github.com/hamdyaea")
        )
    except:
        Crypto.msg = (
            ("CryptoFlouze")
            + str(
                "\n\n\nNo internet connection or daily request limit already reached."
            )
            + str("\n\nDeveloper : Hamdy Abou El Anein\nhttps://github.com/hamdyaea")
        )


start()
