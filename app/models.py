from . import db
from flask_login import UserMixin


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     mobidot_access = db.Column(db.String(150))
#     access_token = db.Column(db.String(150))


class Administrators(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mobidot_access = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(120))
