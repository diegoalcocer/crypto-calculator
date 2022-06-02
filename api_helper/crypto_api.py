import os
import requests
import json
import pandas as pd

currencies = {        
        'BTC':('Bitcoin',"1"),
        'ETH':('Ethereum','1027'),
        'USDT':('Tether','825'),
        'BNB':('binancecoin','1839'),
        'XRP':('Ripple','52'),
        'ADA':('Cardano','2010'),
        'SOL':('Solana','11733'),
        'DOGE':('Dogecoin','74'),
        'DOT':('Polkadot','11517')
        }

def get_current_price(currency_name):
    if currency_name not in currencies:
        return 1

    currency = currencies[currency_name][0]
    currency_id = currencies[currency_name][1]
    url = f"https://api.alternative.me/v2/ticker/{currency}/?convert=USD"
    
    response = requests.get(url).json()
    price = response["data"][currency_id]["quotes"]["USD"]["price"]
    
    return price    