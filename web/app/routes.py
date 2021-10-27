from werkzeug.utils import redirect
from app import app,db
from flask import render_template,url_for,request,flash,session
from app.models import Register
from app.core import Login_user, Register_user
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
        
app.route('/crypto',methods=['GET'])
def crypto():
    return render_template('crypto.html')
