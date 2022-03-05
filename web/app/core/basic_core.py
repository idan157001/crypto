from traceback import TracebackException
from tracemalloc import Traceback
from app.models import *
from hashlib import sha224
import re
import requests
import json
import httpx
import asyncio
#from app.routes import user
import time

from app.core.items import Get_Items

def update_price_coin_db():
    while True:
        get_items_cls = Get_Items('')
        now_price = asyncio.run(get_items_cls.get_eth_btc_price())
        for now_coins in now_price:
            for key,value in now_coins.items():
                coin = db.session.query(Coin_Price).filter_by(name=str(key).upper()).first()
                if coin:
                    coin.price = value
                    db.session.commit()
                    db.session.close()
                    
        
        time.sleep(20) # every x seconds update the db




class Crypto_Info:
    def __init__(self,currency):
        self.currency = currency

    def get_price(self):
        try:
            r = requests.get(f"http://data.messari.io/api/v1/assets/{self.currency}/metrics")
            r = json.loads(r.text)
            price = r['data']['market_data']['price_usd']
            return round(price,2)        
        except Exception as e:
            return 'Error'  
    
    def price_ils(self,c_usd):
        try:
            r = requests.get('https://free.currconv.com/api/v7/convert?q=USD_ILS&compact=ultra&apiKey=a466c0450b716680bf56')
            r = json.loads(r.text)
            return round(float(r['USD_ILS'])*float(c_usd),2)
        except Exception as e:
            print(e)
            return 'Error'  
    def caculate(self,invest,bought,sell):
        try:
            bought = float(bought)
            sell = float(sell)
            invest = float(invest)
        except:
            return False

        precent = (((bought/sell) * 100) -100) * -1
        earn = 0
        earn = invest * (precent/100)
        return (round(precent,2),round(earn,2))
    