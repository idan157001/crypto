from app.models import *
from hashlib import sha224
import re
import requests
import json

        

class Register_user():
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    def valid_email(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if(re.search(regex,self.email)):   
            return True  
        else:   
            return False
    def encrypt_password(self):
        new_password =  sha224(self.password.encode())
        new_password = (new_password.hexdigest())
        return new_password

    def check_uniqe(self):
        if db.session.query(Register).filter_by(username = self.username).first() is None:
        
            if db.session.query(Register).filter_by(email = self.email).first() is None:
                return True

            else:
                return 'Email already in use.' 
        else:
            return 'Username already in use.'


class Login_user():
    def __init__(self,email,password):
        self.email = email
        self.password = (sha224(password.encode())).hexdigest()
    
    def login_check(self):
        object = db.session.query(Register).filter_by(email=self.email).first()
        if object is None:
            return False
        else:
            if object.email == self.email:
                if object.password == self.password:
                    return object.username
            return False
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
            print(e)
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
    
