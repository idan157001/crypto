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

class Register_user():
    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    def valid_email(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if(re.search(regex,self.email)):   
            return True  
        
    def encrypt_password(self):
        new_password =  sha224(self.password.encode())
        new_password = (new_password.hexdigest())
        return new_password

    def check_uniqe(self):
        if not db.session.query(Register).filter_by(username = self.username).first() is None:
            return 'Username already in use.'
        if not db.session.query(Register).filter_by(email = self.email).first() is None:
            return 'Email already in use.' 
        
        return        


class Login_user(Register_user):
    def __init__(self,email,password):
        self.email = email
        self.password = (sha224(password.encode())).hexdigest()
    
    def login_check(self):
        object = db.session.query(Register).filter_by(email=self.email).first()
        if not object:
            return False
       
        if object.email == self.email:
            if object.password == self.password:
                return object.username
        return False