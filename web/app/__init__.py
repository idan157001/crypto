from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

from datetime import timedelta

from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = b'dwa156dwa1d56a1fa61@'
app.permanent_session_lifetime = timedelta(seconds=30)
db = SQLAlchemy(app)


from app import routes,models
