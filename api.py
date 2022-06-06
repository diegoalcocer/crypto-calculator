from collections import namedtuple
import requests




Coin = namedtuple("Coin", "symbol name market_cap_rank current_price high_24h low_24h price_change_24 price_change_7d")

def get_crypto_data() -> Coin:
    base_url = "https://api.coingecko.com/api/v3/coins/markets"
    payload = {"vs_currency":"usd",
               "order":"market_cap_desc",
               "sparkline":"false",
              "price_change_percentage" : "24h,7d,30d"}
    
    data = requests.get(base_url, params = payload)
    json = data.json()
    #print(json)
    coin_list = []
    
    for coin in json:
     
        
        current = Coin(coin["symbol"],
                       coin["name"],
                       coin["market_cap_rank"] ,
                       "{:,}".format(coin["current_price"]) ,
                       coin["high_24h"] ,
                       coin["low_24h"] ,
                       round(coin["price_change_percentage_24h_in_currency"],2) ,
                       round(coin["price_change_percentage_7d_in_currency"],2)      
        )
        
        coin_list.append(current)
        
    return coin_list


     

import api 

def main():
    coins = api.get_crypto_data()
    
    for coin in coins:
        if coin.symbol in ["btc", "eth", "xrp"]:
            print(f"\nThe current price of {coin.name} ({coin.symbol}): {coin.current_price}usd, (24h: {coin.price_change_24}% , 7d: {coin.price_change_7d}%)\n")
   


main()


                   

