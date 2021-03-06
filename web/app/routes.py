from werkzeug.utils import redirect
from app import app,db,limiter
from flask import render_template,url_for,request,flash,session,escape
from app.models import Register,Info
import requests
import asyncio
import json
import time
from datetime import timedelta
import threading
#----------------------------------------

from app.core.authentication import Login_user, Register_user
from app.core.items import Get_Items
from app.core.basic_core import Crypto_Info,update_price_coin_db

#----------------------------------------
t = threading.Thread(target=update_price_coin_db,daemon=True)
t.start()

@app.route('/',methods=['GET'])
@app.route('/home',methods=['GET',])
def home():
        """addr = request.remote_addr
        r = requests.get(f'http://ip-api.com/{addr}')
        print(r.text)"""
        

        return render_template("home.html")

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('user'))
        else:
            return render_template("register.html")

    elif request.method == 'POST':
    
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user = Register_user(username,password,email)
        valid_email = user.valid_email()
        enc_password = user.encrypt_password()
        not_uniqe = user.check_uniqe()

        if len(password) <4:
            flash('Password must be at least 4 characters','error')
            return render_template('register.html')

        if not valid_email:
            flash('Email is not valid.','error')
            return render_template('register.html')

        if not_uniqe:
            flash(user.check_uniqe(),'error')
            return render_template('register.html')
            
        
        new_user = Register(username=username,password=enc_password,email=email)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        flash('Your account has been successfully created!','success')
        
        session['username'] = username
        
        return redirect(url_for('user'))

@app.route('/user')
def user():
    if 'username' in session:
        username = session["username"]
        return render_template('user.html',username=escape(username))
    else:
        return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            flash('You already logged in.')
            return redirect(url_for('user'))
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Login_user(email,password)

        email_valid_check = user.valid_email()
        user_allow_login = user.login_check()
        
        if not email_valid_check:
            flash('Email or password is wrong.','error')
            return render_template('login.html')

        if user_allow_login:
            session['username'] = user_allow_login
            return redirect(url_for('user'))

        flash('Email or password is wrong.','error')
        return render_template('login.html')

@app.route('/logout',methods=['GET'])
def logout():
    if 'username' in session:
        keys = (session.keys())
        session.pop('username')
        session.pop('csrf_token')
    return redirect(url_for('home'))

@app.route('/info',methods=['GET'])
def info():
    return render_template('info.html')
        
@app.route('/crypto',methods=['GET','POST'])
@limiter.limit("1/2second",methods=["POST"])
def crypto():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('crypto.html')

        if request.method == 'POST':
            c_name = request.form['currency']
            if c_name not in ('btc','eth'):
                return render_template('crypto.html')
                 
            Crypto = Crypto_Info(c_name)
            c_value = Crypto.get_price()

            if c_value == 'Error':
                return render_template('crypto.html',ERROR=True)
            
            c_value_ils = Crypto.price_ils(c_value)
            return render_template('crypto.html',c_name=c_name,c_value=c_value,c_value_ils=c_value_ils)
        
    return redirect(url_for('login'))

@app.route('/profit',methods=['GET','POST'])
@limiter.limit("1/2second",methods=["POST"])
def profit():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('profit.html')

        if request.method == 'POST':
            bought_price = request.form['bought_price']
            sell_price = request.form['sell_price']
            my_invest = request.form['my_invest']

            c = Crypto_Info(None)
            caculated = c.caculate(my_invest,bought_price,sell_price)
            if not caculated:
                return render_template('profit.html',error=True)

            return render_template('profit.html',precent=caculated[0],earn=caculated[1])
    return redirect(url_for('login'))


@app.route("/galary",methods=['GET'])
def galary():
    if 'username' in session:
        return render_template("galary.html")
    return redirect(url_for('login'))

@app.route("/items",methods=["GET","POST"])
@limiter.limit("1/2second",methods=["POST"])
def items():
    """
    Wallet
    """
    if "username" in session:
        username = session["username"] 
        classs = Get_Items(username)
        obj = classs.fetch_items_from_db()   
        
        if request.method == "GET":    
            if not obj:
                return render_template("items.html",error="Something went wrong")    
            return render_template("items.html",object=obj[0],percet=obj[1],items_cash=obj[2])

        if request.method == "POST":
            currency = request.form['currency']
            amount = request.form['amount']
            bought = request.form['bought']

            valid = classs.check_valid_form(currency,amount,bought)
            check_max_items = classs.max_items_allowd()

            if len(amount) >10 or len(bought)>10:
                return render_template("items.html",object=obj[0],percet=obj[1],items_cash=obj[2],error="Too much to calculate")

            if not valid:
                return render_template("items.html",object=obj[0],percet=obj[1],items_cash=obj[2],error="Form Not Valid")

            if not check_max_items:
                return render_template("items.html",object=obj[0],percet=obj[1],items_cash=obj[2],error="5 Item is max")
                
            new_item = Info(username=username,coin=currency,amount=amount,bought=bought)
            db.session.add(new_item)
            db.session.commit()
            db.session.close()
            return redirect("/items")
    return redirect(url_for('login'))

@app.route("/items/delete/<id>",methods=["GET","POST"])
def items_remove(id:int):
    print(type(id))
    if "username" in session:
        try:
            int(id)
        except ValueError:
            return render_template("items.html",error="Something went wrong")

        deleted = Get_Items(session['username']).delete_item(id)
        if deleted:
            return redirect("/items")
        else:
            return render_template("items.html",error="Missing Permission")
    return render_template("error.html")

@app.before_request
def before_request_func():
    if "username" in session and "csrf_token" in session:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
        session.modified = True
        
    elif "username" in session and "csrf_token" not in session:
        return redirect("/login")
    #session.permanent = True
    #app.permanent_session_lifetime = timedelta(minutes=3)

@app.errorhandler(429)
def page_not_found(x):
    templates = ('profit','crypto','items')
    page = request.url.split("/")[-1]

    for temp in templates:
        if page == temp:
            if page == "items" and 'username' in session:
                    username = session['username']
                    return render_template(f"{page}.html",spam=True),429
            return render_template(f"{page}.html",spam=True),429

@app.errorhandler(400)
def page_not_found(x):
    if "csrf_token" not in session:
        return render_template("login.html"),400
        
    elif "username" not in session:
        flash("Your session is over\nPlease Relogin ","danger")
        return render_template("login.html"),400
        
@app.errorhandler(404)
def page_not_found(x):
    return render_template("error.html"),404