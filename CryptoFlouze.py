#!/usr/bin/env python3

'''Developer : Hamdy Abou El Anein
https://github.com/hamdyaea'''

# You need to have an free  API key from https://coinmarketcap.com/api/ You have to put it on line 45.

from requests import Session
import json
from easygui import *
import sys
import urllib.request

def start():
    main()
    gui()

def gui():
    image = "./Pictures/crypto.jpg"
    choices = ["Reload"]
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == "Reload":
        start()
    elif reply == "./Pictures/crypto.jpg":
        start()
    else:
        sys.exit(0)
def main():
    global msg
    try:
        urlData = ("https://api.coinpaprika.com/v1/global")
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        global_market = json.loads(data.decode(encoding))
        global_market_cap = (global_market["market_cap_usd"])
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '20',
            'convert': 'USD',
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',  # Enter your https://coinmarketcap.com/api/  api key  here
        }
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        coin = ""
        key = 19
        count = 0
        while count <= key:
            a = str(data["data"][count]["cmc_rank"]) # Rank
            b = str(data["data"][count]["name"]) # Name
            c = str(data["data"][count]["quote"]["USD"]["price"]) # Price
            coin = coin + ((a) + ('{: ^20}'.format(b)) + (c))+str(" $")+str("\n")
            count = count + 1
            if count > key:
                break
        msg = (("                    CryptoFlouze")+str("\n\n               Global Crypto Market Cap   ")\
               +str(global_market_cap)+str(" $")+str("\n\n") + str(coin)\
               +str("\nAll prices are in USD and updated at every run of this software")\
               +str("\n\nDeveloper : Hamdy Abou El Anein\nhttps://github.com/hamdyaea"))
    except:
        msg = (("CryptoFlouze") + str("\n\n\nNo internet connection or daily request limit already reached.")\
               + str("\n\nDeveloper : Hamdy Abou El Anein\nhttps://github.com/hamdyaea"))
start()