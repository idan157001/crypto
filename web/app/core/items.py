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




class Get_Items:
    """
    /items Only
    """
    def __init__(self,username):
        self.username = username


    def get_coins_price_db(self):
        coins = {}
        items = db.session.query(Coin_Price).all()
        for item in items:
            coins.update({item.name:item.price})
        return coins

    def fetch_items_from_db(self):
        from app.core.basic_core import Crypto_Info

        crypto_Info_cls = Crypto_Info('')
        calculated_profit_percet = []
        calculated_profit_cash = []

        items = db.session.query(Info).filter_by(username=self.username).all()
        items = [[item.id,item.coin,item.amount,item.bought]for item in items]
        coins = self.get_coins_price_db()
        try:
            for item in items:
                for name,price in coins.items():
                    
                    if str(item[1]).upper() == name: # ETH || BTC
                        
                        calculated_profit_percet.append(crypto_Info_cls.caculate(invest=item[2],bought=item[3],sell=price)[0])
                        calculated_profit_cash.append(crypto_Info_cls.caculate(invest=item[2],bought=item[3],sell=price)[1])
                    
        except TypeError:
            return False
        return items,calculated_profit_percet,calculated_profit_cash

    def max_items_allowd(self):
        items = db.session.query(Info).filter_by(username=self.username).all()
        if len(items) < 5:
            return True
        return False

    def check_valid_form(self,currency,amount,bought):
        if currency == "btc" or currency == "eth":
            pass
        else:
            return False
        try:
            float(amount)
            float(bought)
            
                
        except:
            return False
        return True
    def delete_item(self,item_id):
        items = db.session.query(Info).filter_by(username=self.username).all()
        for item in items:
            if int(item.id) == int(item_id): 
                db.session.delete(item)
                db.session.commit()
                return True
        return False

    async def get_eth_btc_price_sup(self,client,url):
        resp = await client.get(url)
        
        resp = resp.json()
        price = resp['data']['market_data']['price_usd']
        return {url.split("/assets/")[1].split('/')[0]:round(price,2)}
    async def get_eth_btc_price(self):
        try:
            async with httpx.AsyncClient() as client:
                tasks = []
                for currency in ("btc","eth"):
                    url = f"https://data.messari.io/api/v1/assets/{currency}/metrics"
                    tasks.append(asyncio.ensure_future(self.get_eth_btc_price_sup(client,url)))
                r = await asyncio.gather(*tasks)
            return r
        except Exception as e:
            print("Error!!!!!!!")
            raise e

      

    def caculate_items(self,bought,sell):
        try:
            bought = float(bought)
            sell = float(sell)
        except:
            return False

        precent = (((bought/sell) * 100) -100) * -1
        return round(precent,2)