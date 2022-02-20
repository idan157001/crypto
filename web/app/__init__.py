from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

csrf = CSRFProtect()
csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = b'd0w978975afeaf$eag&faeg156!#$%^$1156dwa1d56a1fa61@'
app.permanent_session_lifetime = timedelta(minutes=10)
db = SQLAlchemy(app)


from app import routes,models
