
from app import db
class Register(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)    
    
    def __repr__(self):
        return f'ID: {self.id}'

    @property
    def info(self):
        return (f'ID: {self.id} Username: {self.username} Password:  {self.password} Email: {self.email}')


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    coin = db.Column(db.String(20), unique=False, nullable=False)
    amount = db.Column(db.Float,nullable=False)
    bought = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"{self.id}"