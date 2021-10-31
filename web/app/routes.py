from werkzeug.utils import redirect
from app import app,db
from flask import render_template,url_for,request,flash,session
from app.models import Register
from app.core import Login_user, Register_user,Crypto_Info
import requests



#----------------------------------------


@app.route('/',methods=['GET'])
@app.route('/home',methods=['GET',])
def home():
        """addr = request.remote_addr
        r = requests.get(f'http://ip-api.com/{addr}')
        print(r.text)"""
        

        return render_template(r"home.html")

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
        check_uniqe = user.check_uniqe()
        if not valid_email:
            flash('Email is not valid.','error')
            return render_template('register.html')

        if check_uniqe != True:

            flash(user.check_uniqe(),'error')
            return render_template('register.html')
        else:
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
        return render_template('user.html',username=username)
    else:
        return redirect(url_for('home'))

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
        user_allow_login = user.login_check()
        if user_allow_login is not False:
            session['username'] = user_allow_login
            return redirect(url_for('user'))
        else:
            flash('Wrong','error')
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
def crypto():
    if request.method == 'GET':
        return render_template('crypto.html')
    if request.method == 'POST':
        c_name = request.form['currency']
        if c_name in ('btc','eth'):
            Crypto = Crypto_Info(c_name)
            c_value = Crypto.get_price()
            if c_value == 'Error':
                return render_template('crypto.html',ERROR=True)
            
            c_value_ils = Crypto.price_ils(c_value)

            return render_template('crypto.html',c_name=c_name,c_value=c_value,c_value_ils=c_value_ils)
        else:
            return render_template('crypto.html')

@app.route('/wallet',methods=['GET','POST'])
def wallet():
    if request.method == 'GET':
        return render_template('wallet.html')
    if request.method == 'POST':
        currency = request.form['currency']
        bought_price = request.form['bought_price']
        sell_price = request.form['sell_price']

        c = Crypto_Info(currency)
        caculated = c.caculate(bought_price,sell_price)
        if caculated is False:
            return render_template('wallet.html')

        return render_template('wallet.html',precent=caculated[0],earn=caculated[1])
