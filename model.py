from extensions import db
from flask_login import UserMixin

class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    User_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    Phone = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(200), nullable=False)
    Created_at = db.Column(db.DateTime, default=db.func.now())

    def get_id(self):
        return self.User_ID

class Request(db.Model):
    __tablename__ = 'request'
    Request_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Phone = db.Column(db.String(20), nullable=False)
    Created_by = db.Column(db.Integer, db.ForeignKey('users.User_ID'))
    Created_at = db.Column(db.DateTime, default=db.func.now())
